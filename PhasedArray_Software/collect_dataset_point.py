import argparse
import os
import numpy as np
import sounddevice as sd
import soundfile as sf

def main():
    # 1. Parse arguments from capture.sh
    parser = argparse.ArgumentParser(description="Hardware capture for Phased Array.")
    parser.add_argument("--code", type=str, required=True)
    parser.add_argument("--duration", type=float, required=True)
    args = parser.parse_args()

    # Configuration: Ensure this matches your hardware!
    SAMPLE_RATE = 44100
    CHANNELS = 4  # Based on your manifest.csv needing Mic1, Mic2, Mic3, Mic4

    # 2. Setup Directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "MICRECORD", args.code, "INDIV")
    os.makedirs(output_dir, exist_ok=True)

    print(f"🎙️ Starting hardware capture for {args.code}...")
    
    try:
        # 3. Record the audio
        # sd.rec records all channels simultaneously into a single 2D numpy array
        recording = sd.rec(int(args.duration * SAMPLE_RATE), 
                           samplerate=SAMPLE_RATE, 
                           channels=CHANNELS, 
                           dtype='float32')
        
        # Block script execution until the recording finishes
        sd.wait() 

        # 4. Split and save the channels
        for i in range(CHANNELS):
            mic_num = i + 1
            filename = f"Mic{mic_num}_{args.code}.wav"
            filepath = os.path.join(output_dir, filename)
            
            # Extract the specific channel (column) from the numpy array
            single_channel_data = recording[:, i]
            
            # Save to standard 16-bit PCM WAV
            sf.write(filepath, single_channel_data, SAMPLE_RATE, subtype='PCM_16')
            print(f"  -> Saved {filename}")
            
        print("✅ Hardware capture complete.")

    except Exception as e:
        print(f"❌ ERROR: Failed to record audio. Details:\n{e}")
        print("\n💡 TROUBLESHOOTING: Run this in a python shell to find your mic's device ID:")
        print("   import sounddevice as sd; print(sd.query_devices())")
        print("   Then add `device=YOUR_DEVICE_ID` to the sd.rec() function.")

if __name__ == "__main__":
    main()