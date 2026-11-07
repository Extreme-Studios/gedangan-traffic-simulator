"""Schema plus relational/provenance checks. Never silently infer missing values."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / 'configuration/schemas'

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def validate_dataset(data):
    schema = load(SCHEMAS/'dataset.schema.json')
    Draft202012Validator(schema).validate(data)
    groups = {name:data[name] for name in schema['$defs']}
    all_ids = [r['id'] for rows in groups.values() for r in rows]
    if len(all_ids) != len(set(all_ids)):
        raise ValueError('IDs must be unique across a dataset.')
    index = {name:{r['id'] for r in rows} for name,rows in groups.items()}
    for name,rows in groups.items():
        for r in rows:
            if r['category'] != data['category']:
                raise ValueError('Data categories must remain separate.')
            if name != 'data_provenance' and r['provenance_id'] not in index['data_provenance']:
                raise ValueError('Missing provenance reference.')
    links = {'road_edges':{'from_node_id':'road_nodes','to_node_id':'road_nodes','lane_ids':'lanes'},
             'road_nodes':{'zone_id':'zones'},'lanes':{'edge_id':'road_edges'},
             'junctions':{'node_id':'road_nodes','incoming_edge_ids':'road_edges','outgoing_edge_ids':'road_edges','signal_id':'traffic_signals'},
             'railway_crossings':{'node_ids':'road_nodes','road_edge_ids':'road_edges','closure_event_source_id':'data_provenance'},
             'zones':{'entry_edge_ids':'road_edges','exit_edge_ids':'road_edges'},
             'od_matrix':{'origin_zone_id':'zones','destination_zone_id':'zones','vehicle_class_id':'vehicle_classes'},
             'traffic_demand':{'od_record_id':'od_matrix'},'traffic_signals':{'junction_id':'junctions'},
             'growth_rates':{'vehicle_class_id':'vehicle_classes','zone_id':'zones'}}
    for name,fields in links.items():
        for r in groups[name]:
            for field,target in fields.items():
                val = r[field]
                refs = val if isinstance(val,list) else ([] if val is None else [val])
                if any(ref not in index[target] for ref in refs):
                    raise ValueError(f'Broken reference: {name}.{field} -> {target}')
    keys = [(r['year'],r['vehicle_class_id'],r['zone_id']) for r in data['growth_rates']]
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate growth rate for year/class/zone.')
    # Reciprocal edge/lane relationships prevent contradictory topology.
    edges = {r['id']:r for r in data['road_edges']}
    for lane in data['lanes']:
        if lane['id'] not in edges[lane['edge_id']]['lane_ids']:
            raise ValueError('Lane missing from parent edge lane_ids.')
    for edge in data['road_edges']:
        for lane_id in edge['lane_ids']:
            if next(r for r in data['lanes'] if r['id']==lane_id)['edge_id'] != edge['id']:
                raise ValueError('Edge/lane parent mismatch.')

def main():
    count=0
    for path in sorted((ROOT/'traffic-data').glob('*/dataset.json')):
        validate_dataset(load(path)); print(f'PASS {path.relative_to(ROOT)}'); count+=1
    schema=load(SCHEMAS/'project.schema.json')
    Draft202012Validator.check_schema(schema)
    Draft202012Validator.check_schema(load(SCHEMAS/'dataset.schema.json'))
    Draft202012Validator(schema).validate(load(ROOT/'configuration/project.json'))
    print(f'PASS project config; {count} category datasets; 2 schemas')

if __name__ == '__main__':
    main()
