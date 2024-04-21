from PIL import Image

def extract_frames(gif_path):
    # Open the GIF file
    gif = Image.open(gif_path)

    # Iterate through each frame of the GIF
    for frame_num in range(gif.n_frames):
        # Seek to the current frame
        gif.seek(frame_num)

        # Convert the frame to RGBA mode
        frame = gif.convert('RGBA')

        # Create a new image with a transparent background
        new_frame = Image.new('RGBA', frame.size, (0, 0, 0, 0))

        # Paste the frame onto the new image
        new_frame.paste(frame, (0, 0), frame)

        # Save the frame as a numbered PNG image
        output_path = f"frame_{frame_num:03d}.png"
        new_frame.save(output_path, format="PNG")

        print(f"Frame {frame_num} saved as {output_path}")

if __name__ == "__main__":
    gif_path = input("Enter the path to the GIF file: ")
    extract_frames(gif_path)
