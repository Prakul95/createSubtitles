#!/bin/bash

# ==== INPUT ARGUMENTS ====
INPUT_PATH="$1"           # e.g., "audio.mp3"
MODEL_SIZE="$2"           # e.g., "base", "medium", "large"
LANGUAGE="$3"             # e.g., "en", "hi", "es"
OUTPUT_FORMAT="$4"        # e.g., "srt", "txt", "vtt"
OUTPUT_DIR="$5"           # e.g., "./output"

# ==== DEFAULT VALUES (if not provided) ====
MODEL_SIZE=${MODEL_SIZE:-"large"}
LANGUAGE=${LANGUAGE:-"en"}
OUTPUT_FORMAT=${OUTPUT_FORMAT:-"srt"}
OUTPUT_DIR=${OUTPUT_DIR:-"./transcripts"}

# ==== CREATE OUTPUT DIR IF NEEDED ====
mkdir -p "$OUTPUT_DIR"

# ==== RUN WHISPER ====
whisper "$INPUT_PATH" \
  --model "$MODEL_SIZE" \
  --language "$LANGUAGE" \
  --task transcribe \
  --output_format "$OUTPUT_FORMAT" \
  --output_dir "$OUTPUT_DIR" \
  --fp16 False \
  --verbose True

echo "✅ Transcription done. Output saved in $OUTPUT_DIR"
