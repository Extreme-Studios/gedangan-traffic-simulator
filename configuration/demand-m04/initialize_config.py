"""Write the initial, editable SYNTHETIC M04 fixtures. Not a survey importer."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REFERENCE='https://eclipse.dev/sumo/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html'
def save(name,data): (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def main():
    rows=[
        ('motorcycle','Sepeda motor','motorcycle',2.1,.8,1.4,16.67,2.0,4.0,7,1.0),
        ('car','Mobil penumpang','passenger',4.5,1.8,1.5,22.22,2.0,4.5,8,2.5),
        ('pickup_van','Pickup dan van','delivery',5.2,1.9,2.1,19.44,1.8,4.0,7,2.5),
        ('minibus','Angkutan umum/minibus','bus',6.0,2.0,2.5,16.67,1.5,4.0,7,2.5),
        ('bus','Bus','bus',12.0,2.5,3.5,16.67,1.2,4.0,7,3.0),
        ('light_truck','Truk ringan','truck',6.5,2.1,2.6,16.67,1.3,4.0,7,3.0),
        ('medium_truck','Truk sedang','truck',8.5,2.4,3.2,16.67,1.1,4.0,7,3.0),
        ('heavy_truck','Truk berat','truck',11.5,2.5,3.8,13.89,.9,4.0,7,3.0),
        ('trailer','Trailer dan kontainer','trailer',16.5,2.55,4.0,13.89,.8,4.0,7,3.5),
        ('oversize','Oversize/khusus','trailer',20.0,3.0,4.5,8.33,.6,3.5,6,4.0),
    ]
    vehicles=[]
    for id,label,vc,length,width,height,speed,accel,decel,emergency,gap in rows:
        params=dict(vClass=vc,length=length,width=width,height=height,maxSpeed=speed,accel=accel,decel=decel,emergencyDecel=emergency,minGap=gap,tau=1.2,sigma=.3,carFollowModel='Krauss',laneChangeModel='LC2013',speedFactor=1.0,speedDev=0.0)
        vehicles.append({'id':id,'label':label,'sumo_vclass':vc,'category':'ASSUMPTION','calibration_status':'NOT_CALIBRATED',
            'parameters':params,'parameter_provenance':{k:{'status':'ASSUMPTION','provenance_id':'A-VEH-01','reason':'Technical test fixture; nominal dimensions/dynamics chosen for size differentiation, not measured Gedangan values. vClass/model mapping follows installed SUMO syntax.'} for k in params},
            'eligibility':{'require_lane_permission':True,'require_source_motor_vehicle_access':True,'allowed_road_functions':['main_arterial_road'] if id in ['bus','medium_truck','heavy_truck','trailer','oversize'] else ['main_arterial_road','frontage_road','feeder_road','collector_road','local_access_road','service_road','connector_road'],
                'require_surveyed_geometry_and_legal_clearance':id=='oversize','minimum_lane_width_m':width+.4,'geometry_status':'ASSUMPTION_SCREEN_ONLY_NOT_SWEPT_PATH','provenance_id':'A-ELIG-01'}})
    save('vehicle-registry.json',{'schema_version':'m04-1','baseline_year':2026,'category':'ASSUMPTION','reference':REFERENCE,'vehicles':vehicles})
    composition={'motorcycle':.20,'car':.40,'pickup_van':.08,'minibus':.06,'bus':.04,'light_truck':.06,'medium_truck':.04,'heavy_truck':.04,'trailer':.04,'oversize':.04}
    save('demand-config.json',{'schema_version':'m04-1','category':'SYNTHETIC_TEST','baseline_year':2026,'seed':20261031,'interval_seconds':900,
        'profiles':{'low':{'requested_per_interval':40,'reason':'First software smoke; fewer than 50 requested, no field meaning.'},'medium':{'requested_per_interval':120,'reason':'Three times low to test conservation/insertion.'},'stress':{'requested_per_interval':300,'reason':'Bounded 300 request software stress, only after smaller runs measured; not peak-hour demand.'}},
        'departure_profile':'uniform_stratified_jitter','composition':composition,'simulation_end_seconds':2100,'step_length_seconds':1,'trajectory_period_seconds':5,
        'year_dimensions':{'baseline_year':2026,'future_growth_records':[],'future_keys':['year','od_id','vehicle_type_id'],'projection_implemented':False},
        'warning_label':'SYNTHETIC TEST — NOT CALIBRATED GEDANGAN TRAFFIC'})
    save('provenance.json',{'records':[{'id':'A-VEH-01','category':'ASSUMPTION','source':REFERENCE,'reason':'Nominal test parameters; syntax checked against installed SUMO 1.28 XSD and parser; not imported default values or survey.'},
        {'id':'A-ELIG-01','category':'ASSUMPTION','reason':'Conservative size screen: large classes arterial only, lane width > vehicle width + .4m. No geometric/permit clearance available for oversize; blocked.'},
        {'id':'A-ZONE-01','category':'ASSUMPTION','reason':'OD anchors use M03 test endpoints and source geometry. Zone boundary and trip distribution are software fixtures, not travel survey.'},
        {'id':'S-DEMAND-01','category':'SYNTHETIC_TEST','reason':'40/120/300 total requests in one 900-second interval; fixed composition and seed. Not observed traffic.'},
        {'id':'R-M03-01','category':'RESEARCH_REFERENCE','source':'simulation/network/m03/network-manifest.json','reason':'Immutable M03 source topology and permissions; OSM-referenced, not field legal verification.'}],
        'observed_records':[],'observed_data_written':False})
    save('od-matrix.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':['schema_version','baseline_year','category','interval_seconds','movements'],
        'properties':{'schema_version':{'const':'m04-1'},'baseline_year':{'const':2026},'category':{'const':'SYNTHETIC_TEST'},'interval_seconds':{'const':900},'movements':{'type':'array','minItems':7,'items':{'type':'object','required':['id','origin_zone','destination_zone','weight','confidence','provenance_id'],'properties':{'id':{'type':'string'},'origin_zone':{'type':'string'},'destination_zone':{'type':'string'},'weight':{'type':'number','exclusiveMinimum':0},'confidence':{'const':'ASSUMPTION'},'provenance_id':{'const':'A-ZONE-01'}}}}}})

if __name__=='__main__':main()
