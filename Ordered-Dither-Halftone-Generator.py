# Python 3.12.4
import numpy as np
import matplotlib.pyplot as plt
import os

def create_circle_image(n):
    # Create blank grid, initialize to 127
    grid = np.full((n, 2 * n), 127, dtype=np.uint8)

    c_x1 = n / 2 - 0.575
    c_y1 = n / 2 - 0.675
    c_x2 = n / 2 - 0.425
    c_y2 = 1.5 * n - 0.675
    radius = n / 2 + 1

    def distance_to_center(i, j, cx, cy):
        return np.sqrt((i - cx)**2 + (j - cy)**2)

   # Fill first half with black circle gradient
    for i in range(n):
        for j in range(n):
            distance = distance_to_center(i, j, c_x1, c_y1)
            if distance <= radius:
                intensity = max(1, int((distance / radius) * 126 + 1))
                grid[i, j] = intensity

    # Fill second half with white circle gradient
    for i in range(n):
        for j in range(n, 2 * n):
            distance = distance_to_center(i, j, c_x2, c_y2)
            if distance <= radius:
                intensity = max(127, int((1 - distance / radius) * 127 + 127))
                grid[i, j] = intensity

    # Rescale values for output
    min_val = grid.min()
    max_val = grid.max()
    divisor =  ((2*n)**2 // 2)
    grid = 1 + np.round((grid - min_val) * ((divisor - 1) / (max_val - min_val)))
    grid = np.clip(grid, 1, divisor)

    return transform_grid(grid)

def transform_grid(grid):
    # Split and reverse halves along x-axis, then merge with original top-down
    left_half = grid[:, :grid.shape[1] // 2]
    right_half = grid[:, grid.shape[1] // 2:]

    transformed_grid = np.hstack((right_half, left_half))

    merged_grid = np.vstack((grid,transformed_grid))

    return np.flipud(merged_grid) # Reverse up/down to regain original order

def print_grid(grid):
    # Find the maximum value in the grid to determine the padding
    max_value = round(np.max(grid))
    print(max_value)
    max_value_length = len(str(max_value))
    
    format_str = f"{{:>{max(max_value_length,3)}}}"
    
    formatted_grid = []
    for row in grid:
        formatted_row =" " * 7 +  " ".join(format_str.format(int(val)) for val in row)
        formatted_grid.append(formatted_row)
    
    return "\n".join(formatted_grid)

def plot_image(grid,dim):
    fig, ax = plt.subplots()
    cax = ax.imshow(grid, cmap='Greens', vmin=0, vmax=grid.max(), interpolation='nearest')

    # Colorbar
    cbar = fig.colorbar(cax, ax=ax, shrink=0.8)
    cbar.set_label('Value')

    # Annotate cells with values
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            ax.text(j, i, int(grid[i, j]), ha='center', va='center', fontsize=2, color='black')

    # Adjust axes to start from 1
    ax.set_xticks(np.arange(grid.shape[1]))
    ax.set_yticks(np.arange(grid.shape[0]))
    ax.set_xticklabels(np.arange(1, grid.shape[1] + 1))
    ax.set_yticklabels(np.arange(1, grid.shape[0] + 1))

    # Set limits
    ax.set_xlim(-0.5, grid.shape[1] - 0.5)

    divisor_final =  ((dim)**2 // 2) + 1
    name = f'h{dim}x{dim}a'
    title = f'{name} div:{divisor_final}'
    plt.title(title)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    subfolder = os.path.join(script_dir, "svg")
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    # save plots
    plt.savefig(os.path.join(subfolder,name + ".svg"), format='svg', bbox_inches='tight')

    plt.close(fig)

output_data = []
output_data.append(f'''  <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Halftones - Angled 45 degrees

  Dynamically generated using ImageMagick-Ordered-Dither-Halftone-Generator

  These patterns initially start as circles, but then form diamonds
  pattern at the 50% threshold level, before forming negated circles,
  as it approached the other threshold extreme.
  -->''')

for n in range(5,26):
    dim = n * 2
    divisor_final =  ((dim)**2 // 2) + 1

    image = create_circle_image(n)
    grid = print_grid(image)
    xml_data = f'''  <threshold map="h{dim}x{dim}a" alias="{dim}x1">
    <description>Halftone {dim}x{dim} (angled)</description>
    <levels width="{dim}" height="{dim}" divisor="{divisor_final}">
{grid}
    </levels>
  </threshold>'''
    print(xml_data)
    output_data.append(xml_data)
    plot_image(image,dim)

script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir,"thresholds.xml"),"w") as f:
    f.write("\n\n".join(output_data))