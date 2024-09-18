# media-datamodel

### Index
 FT.CREATE idx_movie2 on JSON PREFIX 1 movie:
    SCHEMA
       $.original_title as original_title TEXT
       $.day_of_week as day_of_week TAG
       $.budget as budget NUMERIC SORTABLE
       $.runtime as runtime NUMERIC SORTABLE
       $.vote_count as vote_count NUMERIC SORTABLE
       $.year as year NUMERIC


### [Example 1] 
Search any movie
Query --> 
FT.SEARCH idx_movie2 '@original_title: Star' 
FT.SEARCH idx_movie2 '@original_title: Treasure' 


### [Example 2] 
Get all movies having a maximum budget of $ 1M that released on Friday
Query --> 
FT.SEARCH idx_movie2 '@budget:[0 1000000] @day_of_week: {Friday}' RETURN 7 'original_title' 'budget' 'release_date' 'vote_count' 'runtime' 'day_of_week'


### [Example 3] 
Get the maximum votes a movie has received which was released on Friday 
Query -->
FT.aggregate idx_movie2 '@day_of_week: {Friday}' groupby 0 reduce max 1 @vote_count as maximum_votes 


### [Example 4] 
Get the movie which released on Friday and received maximum votes 
Query -->
FT.SEARCH idx_movie2 '@day_of_week: {Friday}' sortby vote_count desc limit 0 1
