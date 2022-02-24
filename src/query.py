query_bq = """

    WITH bounding_box AS (
        SELECT ST_GEOGFROMTEXT('polygon((-3.93455628 40.25387182, -3.93455628 40.57085727, -3.31993445 40.57085727, -3.31993445 40.25387182,-3.93455628 40.25387182))') madrid
    ),
        cinemas as (SELECT 
        ST_UNION_AGG(ST_BUFFER(the_geom,150)) as area
    FROM 
      `carto-ps-bq-developers.data_test.osm_spain_pois`
      where  amenity like '%cinema%'
    )
    select id,lon,lat,amenity,shop,leisure,sport,building,entrance,crossing, the_geom from bounding_box bb, cinemas c,`carto-ps-bq-developers.data_test.osm_spain_pois` r  
    where amenity like '%restaurant%'
    and ST_CONTAINS(c.area,r.the_geom) = FALSE
    and ST_CONTAINS(bb.madrid,r.the_geom)


    """