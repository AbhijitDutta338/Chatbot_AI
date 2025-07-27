import React, { useState } from 'react';
import { Box, Typography, Chip, Card, alpha } from '@mui/material';

const zonesData = {
    "zones": [
        {"zone_id": "z1ha", "zone_name": "Z1HA", "x_coord": 0, "y_coord": 0},
        {"zone_id": "z1hb", "zone_name": "Z1HB", "x_coord": 1, "y_coord": 0},
        {"zone_id": "z1hc", "zone_name": "Z1HC", "x_coord": 2, "y_coord": 0},
        {"zone_id": "z1hd", "zone_name": "Z1HD", "x_coord": 3, "y_coord": 0},
        {"zone_id": "z1he", "zone_name": "Z1HE", "x_coord": 4, "y_coord": 0},
        {"zone_id": "z2ha", "zone_name": "Z2HA", "x_coord": 0, "y_coord": 1},
        {"zone_id": "z2hb", "zone_name": "Z2HB", "x_coord": 1, "y_coord": 1},
        {"zone_id": "z2hc", "zone_name": "Z2HC", "x_coord": 2, "y_coord": 1},
        {"zone_id": "z2hd", "zone_name": "Z2HD", "x_coord": 3, "y_coord": 1},
        {"zone_id": "z2he", "zone_name": "Z2HE", "x_coord": 4, "y_coord": 1},
        {"zone_id": "z3ha", "zone_name": "Z3HA", "x_coord": 0, "y_coord": 2},
        {"zone_id": "z3hb", "zone_name": "Z3HB", "x_coord": 1, "y_coord": 2},
        {"zone_id": "z3hc", "zone_name": "Z3HC", "x_coord": 2, "y_coord": 2},
        {"zone_id": "z3hd", "zone_name": "Z3HD", "x_coord": 3, "y_coord": 2},
        {"zone_id": "z3he", "zone_name": "Z3HE", "x_coord": 4, "y_coord": 2},
        {"zone_id": "z4ha", "zone_name": "Z4HA", "x_coord": 0, "y_coord": 3},
        {"zone_id": "z4hb", "zone_name": "Z4HB", "x_coord": 1, "y_coord": 3},
        {"zone_id": "z4hc", "zone_name": "Z4HC", "x_coord": 2, "y_coord": 3},
        {"zone_id": "z4hd", "zone_name": "Z4HD", "x_coord": 3, "y_coord": 3},
        {"zone_id": "z4he", "zone_name": "Z4HE", "x_coord": 4, "y_coord": 3}
    ]
};

const densityPredictions = {
    'Z1HA': 2.95, 'Z1HB': 2.95, 'Z1HC': 5.32, 'Z1HD': 2.94, 'Z1HE': 2.09, 
    'Z2HA': 2.03, 'Z2HB': 2.94, 'Z2HC': 6.55, 'Z2HD': 2.24, 'Z2HE': 1.89, 
    'Z3HA': 2.17, 'Z3HB': 2.8,  'Z3HC': 3.19, 'Z3HD': 2.24, 'Z3HE': 1.98, 
    'Z4HA': 1.29, 'Z4HB': 1.91, 'Z4HC': 1.95, 'Z4HD': 1.89, 'Z4HE': 1.29
};

const getDensityLevel = (density) => {
    if (density > 5) return 'high';
    if (density >= 2 && density <= 5) return 'medium';
    return 'low';
};

const getDensityColor = (level) => {
    switch (level) {
        case 'high': return '#f44336'; // Red
        case 'medium': return '#ff9800'; // Orange
        case 'low': return '#4CAF50'; // Green
        default: return '#9E9E9E'; // Grey
    }
};

const getDensityGradient = (level) => {
    switch (level) {
        case 'high': return '#f44336';
        case 'medium': return '#ff9800';
        case 'low': return '#4CAF50';
        default: return '#9E9E9E';
    }
};

const getDensityLabel = (level) => {
    switch (level) {
        case 'high': return 'High Density';
        case 'medium': return 'Medium Density';
        case 'low': return 'Low Density';
        default: return 'Unknown';
    }
};

const Heatmap = () => {
    const [selectedZone, setSelectedZone] = useState(null);
    
    // Create a 4x5 grid for mobile display
    const createGrid = () => {
        const grid = Array(4).fill(null).map(() => Array(5).fill(null));
        zonesData.zones.forEach(zone => {
            grid[zone.y_coord][zone.x_coord] = zone;
        });
        return grid;
    };

    const grid = createGrid();

    const handleZoneClick = (zone) => {
        setSelectedZone(selectedZone === zone.zone_name ? null : zone.zone_name);
    };

    return (
        <Box sx={{ width: '100%', maxWidth: 400, mx: 'auto' }}>
            {/* Legend */}
            <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-around', flexWrap: 'wrap', gap: 0.5 }}>
                    <Chip 
                        size="small" 
                        label="Low Density" 
                        sx={{ 
                            bgcolor: getDensityColor('low'), 
                            color: 'white',
                            fontSize: '0.7rem',
                            height: 24
                        }} 
                    />
                    <Chip 
                        size="small" 
                        label="Medium Density" 
                        sx={{ 
                            bgcolor: getDensityColor('medium'), 
                            color: 'white',
                            fontSize: '0.7rem',
                            height: 24
                        }} 
                    />
                    <Chip 
                        size="small" 
                        label="High Density" 
                        sx={{ 
                            bgcolor: getDensityColor('high'), 
                            color: 'white',
                            fontSize: '0.7rem',
                            height: 24
                        }} 
                    />
                </Box>
            </Box>

            {/* Heatmap Grid */}
            <Box sx={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(5, 1fr)', 
                gridTemplateRows: 'repeat(4, 1fr)',
                gap: 0.7,
                aspectRatio: '5/4',
                maxHeight: 160
            }}>
                {grid.map((row, rowIndex) => 
                    row.map((zone, colIndex) => {
                        if (!zone) return <Box key={`${rowIndex}-${colIndex}`} />;
                        
                        const density = densityPredictions[zone.zone_name];
                        const level = getDensityLevel(density);
                        const color = getDensityColor(level);
                        const isSelected = selectedZone === zone.zone_name;
                        
                        return (
                            <Card
                                key={zone.zone_id}
                                elevation={isSelected ? 4 : 1}
                                onClick={() => handleZoneClick(zone)}
                                sx={{
                                    bgcolor: color,
                                    color: 'white',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    cursor: 'pointer',
                                    fontSize: '0.7rem',
                                    fontWeight: 'bold',
                                    textShadow: '1px 1px 2px rgba(0,0,0,0.5)',
                                    transition: 'all 0.2s ease-in-out',
                                    transform: isSelected ? 'scale(1.05)' : 'scale(1)',
                                    border: isSelected ? '2px solid #333' : 'none',
                                    minWidth: '70px',
                                    '&:hover': {
                                        transform: 'scale(1.1)',
                                        elevation: 3,
                                        zIndex: 1
                                    }
                                }}
                            >
                                {zone.zone_name}
                            </Card>
                        );
                    })
                )}
            </Box>

            {/* Selected Zone Info */}
            {selectedZone && (
                <Box sx={{ mt: 2, textAlign: 'center' }}>
                    <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
                        <strong>{selectedZone}:</strong> {getDensityLabel(getDensityLevel(densityPredictions[selectedZone]))} 
                        ({densityPredictions[selectedZone].toFixed(2)})
                    </Typography>
                </Box>
            )}
        </Box>
    );
};

export default Heatmap;
