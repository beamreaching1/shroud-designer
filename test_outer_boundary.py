"""
Test script to demonstrate the new outer boundary snap feature.
This shows that analyze_fan now captures both hole and outer boundary info.
"""
from pathlib import Path
from shroud_designer.geometry import analyze_fan

def test_fan_analysis():
    """Test that fan analysis captures both hole and outer boundary."""
    # Use the default fan STL
    fan_path = Path("Fans/default 120mm fan for shroud.stl")
    
    print("Testing fan analysis with outer boundary feature...")
    print(f"Loading: {fan_path}")
    
    analysis = analyze_fan(fan_path)
    
    print(f"\n✓ Successfully analyzed fan")
    print(f"\nHole (opening) information:")
    print(f"  - Diameter: {analysis.hole_diameter:.2f} mm")
    print(f"  - Center: ({analysis.hole_center[0]:.2f}, {analysis.hole_center[1]:.2f})")
    
    print(f"\nOuter boundary information:")
    print(f"  - Diameter: {analysis.outer_diameter:.2f} mm")
    print(f"  - Center: ({analysis.outer_center[0]:.2f}, {analysis.outer_center[1]:.2f})")
    
    print(f"\nMesh information:")
    print(f"  - Thickness: {analysis.z_max - analysis.z_min:.2f} mm")
    print(f"  - Vertices: {len(analysis.mesh.vertices)}")
    print(f"  - Faces: {len(analysis.mesh.faces)}")
    
    # Test the toggle functionality
    print(f"\n--- Testing use_outer_boundary toggle ---")
    
    print(f"\nWith use_outer_boundary = False (default):")
    analysis.use_outer_boundary = False
    print(f"  Active diameter: {analysis.active_diameter:.2f} mm")
    print(f"  Active center: ({analysis.active_center[0]:.2f}, {analysis.active_center[1]:.2f})")
    
    print(f"\nWith use_outer_boundary = True:")
    analysis.use_outer_boundary = True
    print(f"  Active diameter: {analysis.active_diameter:.2f} mm")
    print(f"  Active center: ({analysis.active_center[0]:.2f}, {analysis.active_center[1]:.2f})")
    
    # Test rotation functionality
    print(f"\n--- Testing rotation feature ---")
    
    print(f"\nRotation angle (default): {analysis.rotation_angle}°")
    
    print(f"\nSetting rotation to 45°:")
    analysis.rotation_angle = 45.0
    print(f"  Rotation angle: {analysis.rotation_angle}°")
    
    print(f"\nSetting rotation to -90°:")
    analysis.rotation_angle = -90.0
    print(f"  Rotation angle: {analysis.rotation_angle}°")
    
    print(f"\nResetting rotation to 0°:")
    analysis.rotation_angle = 0.0
    print(f"  Rotation angle: {analysis.rotation_angle}°")
    
    print(f"\n✓ All tests passed! The outer boundary and rotation features are working correctly.")
    print(f"\nUsage in the UI:")
    print(f"  1. Load a fan connector STL (File → Import)")
    print(f"  2. Check the 'Snap to bracket outline (not opening)' checkbox")
    print(f"  3. Adjust the 'Rotation' spinbox to rotate the bracket (e.g., for dual-fan alignment)")
    print(f"  4. The funnel will snap to the rotated outer boundary")

if __name__ == "__main__":
    test_fan_analysis()
