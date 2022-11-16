"""
Example of spatial NSRP modelling based on a catchment in the Rhine basin.

Script version of stnsrp_example.ipynb notebook.

"""

import rwgen

# Boilerplate line needed to use multiprocessing in fitting on Windows OS
if __name__ == '__main__':

    # Initialise model
    rainfall_model = rwgen.RainfallModel(
        spatial_model=True,
        project_name='upper_rhine',
        intensity_distribution='weibull',
        point_metadata='./input/gauge_metadata.csv',
    )

    # Preprocessing using trimming
    rainfall_model.preprocess(
        input_timeseries='./input/gauge_data',
        outlier_method='trim',
        # output_filenames={'statistics': 'reference_statistics2.csv'},
    )

    # Fitting with bounds for some parameters and fixed values for others
    rainfall_model.fit(
        n_workers=6,  # for a 6-core computer
        parameter_bounds='./input/fitting/parameter_bounds.csv',
        fixed_parameters='./input/fitting/fixed_parameters.csv',
    )

    # Simulate with both point and catchment output
    rainfall_model.simulate(
        output_types=['point', 'catchment'],
        catchment_metadata='./input/catchments.shp',
        epsg_code=32632,
        cell_size=1000.0,
        dem='./input/srtm_dem.asc',
        simulation_length=500,
        n_realisations=2,
    )

    # Postprocessing
    rainfall_model.postprocess(
        amax_durations=[1, 3, 6, 24],
        ddf_return_periods=[2, 5],
    )

    # Plotting
    rainfall_model.plot(point_id=3)
    rainfall_model.plot(plot_type='cross-correlation')

