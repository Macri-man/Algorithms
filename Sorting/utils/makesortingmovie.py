import numpy as np
import matplotlib.pyplot as plt
import ffmpeg
import os

# Import sorting algorithms
from BubbleSort.iteration import bubble_sort_iterative
from TimSort.iteration import tim_sort_iterative
from InsertionSort.iteration import insertion_sort_iterative
from SelectionSort.iteration import selection_sort_iterative
from MergeSort.iteration import merge_sort_iterative
from QuickSort.iteration import quick_sort_iterative
from HeapSort.iteration import heap_sort_iterative
from CountingSort.iteration import counting_sort_iterative
from ShellSort.iteration import shell_sort_iterative
from RadixSort.iteration import radix_sort_iterative

class SortingVisualizer:
    def __init__(self, arr_size=100, output_dir="sorting_videos"):
        self.arr_size = arr_size
        self.output_dir = output_dir
        self.sorting_algorithms = {
            "Bubble Sort": bubble_sort_iterative,
            "Tim Sort": tim_sort_iterative,
            "Insertion Sort": insertion_sort_iterative,
            "Selection Sort": selection_sort_iterative,
            "Merge Sort": merge_sort_iterative,
            "Quick Sort": quick_sort_iterative,
            "Heap Sort": heap_sort_iterative,
            "Counting Sort": counting_sort_iterative,
            "Shell Sort": shell_sort_iterative,
            "Radix Sort": radix_sort_iterative
        }
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "Videos"), exist_ok=True)        


    def update(self, arr, algorithm_name, step, frames_dir):
        """Captures the current state of the sorting process as an image."""
        # Set a fixed figure size to ensure consistency across all frames
        fig, ax = plt.subplots(figsize=(8, 6))  # (width, height)
        
        # Plot the array as a bar chart
        ax.bar(range(len(arr)), arr, color='black')
        
        # Set plot labels and title
        ax.set_title(f"{algorithm_name} - Step {step}")
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        
        # Set consistent Y-axis limits, with a margin of 1 to ensure visibility of all values
        ax.set_ylim(0, max(arr) + 1)
        
        # Optionally, set consistent X-axis limits to avoid shifting bar positions
        ax.set_xlim(-0.5, len(arr) - 0.5)
        
        # Save the figure to the specified directory with the step number
        frame_filename = f"{frames_dir}/frame_{step}.png"
        plt.savefig(frame_filename)
        plt.close(fig)


    def visualize_sorting(self, algorithm_name, sort_function):
        """Runs a specific sorting algorithm and captures frames for animation."""
        frames_dir = os.path.join(self.output_dir, algorithm_name.replace(" ", "_"))
        print("Frames Directory visualize:", os.path.abspath(frames_dir))
    
        os.makedirs(frames_dir, exist_ok=True)
        

        original_arr = np.random.randint(1, 1000, size=self.arr_size)
        arr = original_arr.copy()
        step = 0
        
        def capture(arr_copy):  # Wrapper for update function
            nonlocal step
            self.update(arr_copy, algorithm_name, step, frames_dir)
            step += 1

        print(f"Running {algorithm_name}...")
        sort_function(arr, capture)  # Execute sorting with visualization
        print(f"{algorithm_name} completed!")

    def create_video(self, algorithm_name):
        """Generates an MP4 video from the captured frames for a specific algorithm."""
        try:
            frames_dir = os.path.join(self.output_dir, algorithm_name.replace(" ", "_"))
            input_pattern = os.path.join(frames_dir,"frame_%d.png")
            output_file = os.path.join(self.output_dir, "Videos", f"{algorithm_name.replace(' ', '_')}.mp4")

           


            # Print full paths for debugging
            print("Frames Directory:", os.path.abspath(frames_dir))
            print("Input Pattern:", os.path.abspath(input_pattern))
            print("Output File:", os.path.abspath(output_file))

            ffmpeg.input(input_pattern, framerate=10).output(output_file, vcodec='libx264', pix_fmt='yuv420p', ss=0).run(overwrite_output=True)

            print(f"MP4 video for {algorithm_name} created successfully!")

        except ffmpeg.Error as e:
            print(f"An error occurred while generating the video for {algorithm_name}.")
            print(f"Error details: {e.stderr.decode()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def cleanup_frames(self):
        """Deletes all generated frame images after video creation."""
        for algorithm_name in self.sorting_algorithms.keys():
            frames_dir = os.path.join(self.output_dir, algorithm_name.replace(" ", "_"))
            print("Frames Directory cleanup:", os.path.abspath(frames_dir))
            self.delete_folder_contents(frames_dir)
            os.rmdir(frames_dir)
        print("Cleanup completed!")

    
    def delete_folder_contents(self, folder_path):
        """Deletes the contents of a folder recursively."""
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)  # Delete file or symlink
                    elif os.path.isdir(file_path):
                        self.delete_folder_contents(file_path)  # Recursively delete contents
                        os.rmdir(file_path)  # Remove empty subdirectory
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

    def run(self):
        """Runs the full sorting visualization pipeline for each sorting algorithm."""
        self.delete_folder_contents(os.path.join(self.output_dir, "Videos"))
        for algorithm_name, sort_function in self.sorting_algorithms.items():
            self.visualize_sorting(algorithm_name, sort_function)  # Visualize each algorithm
            self.create_video(algorithm_name)  # Create a video for each algorithm
        self.cleanup_frames()  # Clean up all frames after videos are generated

# Run the visualization
if __name__ == "__main__":
    visualizer = SortingVisualizer()
    visualizer.run()
