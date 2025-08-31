#!/usr/bin/env python3
"""
CTF Flag Decoder for 'Echoes in the Deep' Challenge
"""

def decode_flag():
    """Extract and decode the hidden flag from the audio file"""
    
    # Open the WAV file and extract audio data
    with open('deep_secrets.wav', 'rb') as f:
        f.seek(44)  # Skip WAV header
        data = f.read()
    
    print(f"Audio data size: {len(data)} bytes")
    
    # Based on analysis, we found CTF at position 1143295
    # Let's try a different approach - extract data at regular intervals
    
    # Method 1: Extract every 1000th byte and look for patterns
    print("\n=== Method 1: Every 1000th byte ===")
    extracted_1000 = []
    for i in range(0, len(data), 1000):
        if 32 <= data[i] <= 126:
            extracted_1000.append(chr(data[i]))
        else:
            extracted_1000.append('.')
    
    result_1000 = ''.join(extracted_1000)
    print(f"Every 1000th character: {result_1000}")
    
    # Method 2: Look for flag by analyzing ASCII sequences
    print("\n=== Method 2: ASCII Sequence Analysis ===")
    ascii_sequences = []
    current_seq = ''
    
    for b in data:
        if 32 <= b <= 126:
            current_seq += chr(b)
        else:
            if len(current_seq) > 5:
                ascii_sequences.append(current_seq)
            current_seq = ''
    
    # Look for sequences that might be the flag
    flag_candidates = []
    for seq in ascii_sequences:
        if any(pattern in seq.lower() for pattern in ['flag', 'ctf', '_', '{']):
            flag_candidates.append(seq)
    
    print(f"Found {len(flag_candidates)} potential flag sequences:")
    for i, candidate in enumerate(flag_candidates[:10]):
        print(f"{i+1}: {candidate}")
    
    # Method 3: Try decoding specific sequences we found
    print("\n=== Method 3: Decode Specific Sequences ===")
    
    # The sequence "GTP_:s:0DMGRP" looks promising
    suspicious = "GTP_:s:0DMGRP"
    print(f"Analyzing: {suspicious}")
    
    # Try different decoding methods
    decodings = []
    
    # ROT13
    rot13 = ''
    for char in suspicious:
        if 'A' <= char <= 'Z':
            rot13 += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
        elif 'a' <= char <= 'z':
            rot13 += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
        else:
            rot13 += char
    decodings.append(("ROT13", rot13))
    
    # Character substitution
    char_map = {
        'G': 'f', 'T': 'l', 'P': 'a', '_': '_',
        ':': 'g', 's': '{', '0': 'o', 'D': 'd', 'M': 'e', 'R': 'e', 'P': 'p'
    }
    
    # Try another approach - maybe it's a simple substitution
    # Let's try: G->f, T->l, P->a, etc.
    
    # Actually, let me try a different approach
    # What if "GTP_:s:0DMGRP" when properly decoded becomes something like "flag{xxx_xxx_xxx}"?
    
    # Let's try treating it as a cipher where:
    # GTP_ -> flag
    # :s:0 -> {xxx
    # DMGRP -> _xxx}
    
    print("Trying manual cipher analysis...")
    
    # Method 4: Look at the data around CTF position more carefully
    print("\n=== Method 4: CTF Position Analysis ===")
    ctf_pos = 1143295
    
    # Extract larger context around CTF
    start = max(0, ctf_pos - 1000)
    end = min(len(data), ctf_pos + 1000)
    context = data[start:end]
    
    # Convert to ASCII and look for patterns
    context_ascii = ''
    for b in context:
        if 32 <= b <= 126:
            context_ascii += chr(b)
        else:
            context_ascii += '.'
    
    print(f"Context around CTF (length {len(context_ascii)}):")
    print(context_ascii)
    
    # Look for flag pattern in the context
    if 'flag{' in context_ascii.lower():
        flag_start = context_ascii.lower().find('flag{')
        potential_flag = context_ascii[flag_start:flag_start+50]
        print(f"\n*** FOUND FLAG: {potential_flag} ***")
        return potential_flag
    
    # Method 5: Try extracting from specific positions
    print("\n=== Method 5: Positional Extraction ===")
    
    # Try extracting every nth character starting from different positions
    for start_offset in [0, 100, 500, 1000]:
        for step in [1000, 2000, 5000]:
            extracted = []
            pos = start_offset
            while pos < len(data) and len(extracted) < 50:
                if 32 <= data[pos] <= 126:
                    extracted.append(chr(data[pos]))
                pos += step
            
            result = ''.join(extracted)
            if 'flag' in result.lower():
                print(f"*** FOUND FLAG at offset {start_offset}, step {step}: {result} ***")
                return result
    
    print("\nNo clear flag found with standard methods. The flag might be encoded differently.")
    return None

if __name__ == "__main__":
    flag = decode_flag()
    if flag:
        print(f"\n🎉 SUCCESS! The flag is: {flag}")
    else:
        print("\n❌ Could not decode the flag automatically.")