--  This script lists all bands with Glam rock
-- as their main style, ranked by their longevity

SELECT band_name,
    CASE
        WHEN split IS NULL THEN 2022 - formed
        ElSE split - formed
    END AS lifespan
FROM metal_bands
ORDER BY lifespan DESC;
