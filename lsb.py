from PIL import Image
import numpy as np

def text_to_bits(text):
    return ''.join(f'{ord(c):08b}' for c in text)
def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message = ''
    for b in chars:
        if b == '00000000':  
            break
        message += chr(int(b, 2))
    return message

def hide_message(image_path, message, output_path):
    image = Image.open(image_path)
    pixels = np.array(image)
    h, w, _ = pixels.shape

    message_bits = text_to_bits(message) + '00000000'  
    total_bits = len(message_bits)

    flat_pixels = pixels.reshape(-1, 3)  
    print(flat_pixels.shape[0])

    if total_bits > flat_pixels.shape[0] * 3:
        raise ValueError("Message too long to hide in this image.")

    bit_idx = 0
    for i in range(flat_pixels.shape[0]):
        for j in range(3):  # For R, G, B
            if bit_idx < total_bits:
                flat_pixels[i, j] &= 0b11111110  # Clear LSB
                flat_pixels[i, j] |= int(message_bits[bit_idx])  # Set LSB to message bit
                bit_idx += 1
            else:
                break

    new_pixels = flat_pixels.reshape((h, w, 3))
    stego_image = Image.fromarray(new_pixels.astype('uint8'))
    stego_image.save(output_path)

def extract_message(image_path):
    image = Image.open(image_path)
    pixels = np.array(image)
    flat_pixels = pixels.reshape(-1, 3)  # Flatten (height * width, 3)

    bits = ''
    for i in range(flat_pixels.shape[0]):
        for j in range(3):  # R, G, B channels
            bits += str(flat_pixels[i, j] & 1)  # Get LSB
            if bits.endswith('00000000'):  # Stop at null terminator
                return bits_to_text(bits)

    return bits_to_text(bits)

# print(extract_message('static/encoded_images/cat.jpeg'))