"""No placeholder metric is a measurement. Unknown metrics remain null."""
class MetricsCollector:
    def snapshot(self):
        return {'run_id': None, 'category': 'simulated_results', 'queue_length_m': None,
                'travel_time_s': None, 'density_vehicles_per_km': None,
                'speed_m_per_s': None, 'capacity_vehicles_per_hour': None,
                'status': 'NO_SIMULATION_RESULTS'}
