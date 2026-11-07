"""Rebuild JSON Schema contracts, without creating any traffic measurements."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STR = {'type': 'string', 'minLength': 1}
REF = {**STR}
NULLSTR = {'type': ['string','null']}
NUM = {'type': ['number','null'], 'minimum': 0}
ARRREF = {'type': 'array', 'items': REF, 'uniqueItems': True}
CLASSES = ['motorcycle','car','bus','truck','trailer','oversize_special']
CATEGORIES = ['observed_data','research_reference','assumptions','simulated_results']

def obj(props, required=None):
    return {'type':'object','additionalProperties':False,'properties':props,'required':list(props) if required is None else required}

common = {'id': STR, 'category': {'enum':CATEGORIES}, 'provenance_id': REF,
          'calibration_status': {'enum':['unverified','verified','not_started','in_progress','calibrated','rejected']}}

def record(fields):
    return obj({**common, **fields})

defs = {
 'road_nodes': record({'x_m':{'type':['number','null']},'y_m':{'type':['number','null']},'crs':NULLSTR,'zone_id':NULLSTR}),
 'road_edges': record({'from_node_id':REF,'to_node_id':REF,'lane_ids':ARRREF,'corridor_role':{'enum':['main','frontage','access','other','unverified']},'length_m':NUM,'speed_limit_m_per_s':NUM,'capacity_vehicles_per_hour':NUM}),
 'lanes': record({'edge_id':REF,'index':{'type':'integer','minimum':0},'width_m':NUM,'allowed_vehicle_classes':{'type':'array','items':{'enum':CLASSES},'uniqueItems':True}}),
 'junctions': record({'node_id':REF,'incoming_edge_ids':ARRREF,'outgoing_edge_ids':ARRREF,'control_type':{'enum':['signal','priority','uncontrolled','unverified']},'signal_id':NULLSTR}),
 'railway_crossings': record({'node_ids':ARRREF,'road_edge_ids':ARRREF,'track_count':{'type':['integer','null'],'minimum':1},'closure_event_source_id':NULLSTR,'station_interaction_notes':NULLSTR}),
 'vehicle_classes': record({'class':{'enum':CLASSES},'sumo_vclass':NULLSTR,'length_m':NUM,'width_m':NUM,'max_speed_m_per_s':NUM,'behavior_profile_id':NULLSTR}),
 'zones': record({'name':STR,'boundary_geojson':NULLSTR,'entry_edge_ids':ARRREF,'exit_edge_ids':ARRREF}),
 'od_matrix': record({'year':{'type':'integer','minimum':2026},'origin_zone_id':REF,'destination_zone_id':REF,'vehicle_class_id':REF,'period_start':STR,'period_end':STR,'trips':{'type':['integer','null'],'minimum':0}}),
 'traffic_demand': record({'od_record_id':REF,'departure_profile':{'enum':['unverified','observed','documented_assumption']},'vehicles_per_hour':NUM,'period_start':STR,'period_end':STR}),
 'traffic_signals': record({'junction_id':REF,'cycle_s':NUM,'phases':{'type':'array','items':obj({'state':STR,'duration_s':NUM})},'offset_s':NUM}),
 'infrastructure_scenarios': record({'name':STR,'baseline_dataset_id':REF,'parent_scenario_id':NULLSTR,'changes':{'type':'array','items':obj({'entity_type':{'enum':['road_edges','lanes','junctions','railway_crossings','traffic_signals']},'entity_id':REF,'parameter':STR,'before':{'type':['string','number','boolean','null']},'after':{'type':['string','number','boolean','null']},'provenance_id':REF})},'approval_status':{'enum':['draft','reviewed','approved']}}),
 'simulation_metrics': record({'run_id':REF,'scenario_id':REF,'network_hash':STR,'demand_hash':STR,'seed':{'type':'integer'},'sumo_version':STR,'year':{'type':'integer','minimum':2026},'interval_start_s':NUM,'interval_end_s':NUM,'edge_id':NULLSTR,'queue_length_m':NUM,'travel_time_s':NUM,'density_vehicles_per_km':NUM,'speed_m_per_s':NUM,'capacity_vehicles_per_hour':NUM}),
 'data_provenance': obj({'id':STR,'category':{'enum':CATEGORIES},'source_title':STR,'source_uri':STR,'source_year':{'type':['integer','null']},'accessed_on':{'type':'string','pattern':r'^\d{4}-\d{2}-\d{2}$'},'survey_period':NULLSTR,'method':NULLSTR,'spatial_scope':NULLSTR,'license_notes':NULLSTR,'verification_status':{'enum':['unverified','metadata_checked','abstract_checked','full_context_checked','field_verified']},'limitations':STR}),
 'calibration_status': record({'target_entity_type':STR,'target_entity_id':REF,'method':NULLSTR,'observed_dataset_id':NULLSTR,'validation_dataset_id':NULLSTR,'acceptance_criteria':NULLSTR,'reviewer':NULLSTR,'reviewed_on':NULLSTR}),
 'growth_rates': record({'year':{'type':'integer','minimum':2027},'vehicle_class_id':REF,'zone_id':REF,'annual_rate':{'type':['number','null'],'minimum':-1},'rate_unit':{'const':'fraction_per_year'},'method':NULLSTR})
}
schema = {'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:gedangan:dataset:0.1.0',
          **obj({'schema_version':{'const':'0.1.0'},'dataset_id':STR,'baseline_year':{'const':2026},'category':{'enum':CATEGORIES},
                 **{name:{'type':'array','items':{'$ref':f'#/$defs/{name}'}} for name in defs}}), '$defs':defs}
out = ROOT / 'configuration' / 'schemas'
out.mkdir(exist_ok=True)
(out/'dataset.schema.json').write_text(json.dumps(schema,indent=2)+'\n',encoding='utf-8')
# Config is intentionally bounded; no implied growth, seed, or simulation timestep.
config = json.loads((ROOT/'configuration/project.json').read_text(encoding='utf-8'))
config_schema = {'$schema':schema['$schema'],'$id':'urn:gedangan:project:0.1.0',**obj({
 'project':{'const':config['project']},'version':{'const':'0.1.0'},'milestone':{'const':1},'baseline_year':{'const':2026},'mode':{'const':'FOUNDATION'},'engine':{'const':'ENGINE NOT CONNECTED'},
 'network_path':{'type':'null'},'demand_path':{'type':'null'},'calibration_status':{'const':'not_started'},
 'growth':obj({'baseline_year':{'const':2026},'rates':{'type':'array','items':{'$ref':'#/$defs/growth_rates'}},'missing_rate_policy':{'const':'error'},'rate_unit':{'const':'fraction_per_year'},'dimensions':{'const':['year','vehicle_class_id','zone_id']},'formula_future':STR}),
 'simulation':obj({k:{'type':'null'} for k in config['simulation']}),
 'visualization':obj({'scene':{'const':'abstract_placeholder_not_geographic'},'pixel_ratio_cap':{'type':'number','minimum':1,'maximum':1.5},'render_fps_cap':{'type':'integer','minimum':1,'maximum':30},'external_assets':{'const':False}}),
 'target':obj({'os':STR,'gpu':STR,'vram_gb':{'type':'number','minimum':1},'ram_gb':{'type':'number','minimum':1},'resolution':STR})}), '$defs':{'growth_rates':defs['growth_rates']}}
(out/'project.schema.json').write_text(json.dumps(config_schema,indent=2)+'\n',encoding='utf-8')
print('Built dataset.schema.json and project.schema.json')
