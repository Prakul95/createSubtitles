import subprocess
import srt
from faster_whisper import WhisperModel

from datetime import timedelta
import os

class whisper_internal:
    def __init__(self, backend="whisper", model_size="base", **kwargs):
        self.backend = backend
        self.model_size = model_size
        self.kwargs = kwargs
        self.script_path = self._load_model()
        self.input_path = kwargs.get("input_path", "")
        self.language = kwargs.get("language", "en")
        self.task = kwargs.get("task", "transcribe")
        self.beam_size = kwargs.get("beam_size", 1)
        self.word_timestamps = kwargs.get("word_timestamps", False)
        self.output_format = kwargs.get("output_format", "srt")
        self.output_dir = kwargs.get("output_dir", "")
        self.verbose = kwargs.get("verbose", True)
        
    def transcribeFastWhisper(self):
        if not self.input_path or not os.path.isfile(self.input_path):
            print("❌ Invalid or missing input file:", self.input_path)
            return

        print(f"🚀 Running Faster-Whisper on {self.input_path} with model {self.model_size}")

    # Transcribe using the model
        segments, info = self.model.transcribe(
            self.input_path,
            beam_size=int(self.beam_size),
            language=self.language,
            word_timestamps=self.word_timestamps
            )

    # Convert segments to SRT
        subs = []
        delay = 1  # delay in seconds
        for i, segment in enumerate(segments):
            start = timedelta(seconds=segment.start + delay)
            end = timedelta(seconds=segment.end + delay)
            text = segment.text.strip()
            subs.append(srt.Subtitle(index=i + 1, start=start, end=end, content=text))

    # Output filename (based on input)
        base_name = os.path.splitext(os.path.basename(self.input_path))[0]
        default_output_dir = os.path.dirname(self.input_path)  # same folder as input

        output_dir = self.output_dir if hasattr(self, 'output_dir') and self.output_dir else default_output_dir
        output_path = os.path.join(output_dir, f"{base_name}.srt")

        os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(srt.compose(subs))

        print(f"✅ Subtitles saved to: {output_path}")



        
    def _load_model(self):
        if self.backend == "whisper":
            script_path = "./run_whisper.sh"
            # self.model_size = self.kwargs.get("model_size", "large")
            # self.language = self.kwargs.get("language", "en")
            # self.beam_size = self.kwargs.get("beam_size", 1)
            
        elif self.backend == "faster-whisper":
            self.model = WhisperModel(self.model_size, compute_type="int8")
            script_path = "Running Fast whisper model"
            # self.model_size = self.kwargs.get("model_size", "large")
            # self.language = self.wargs.get("language", "en")
            # self.beam_size = self.kwargs.get("beam_size", 1)
        else:
            raise ValueError("Unsupported backend. Use 'whisper' or 'faster-whisper'.")
        return script_path

        


def callBashFunction(backend="whisper", model_size="base", **kwargs):
    obj = whisper_internal(backend, model_size, **kwargs)
    # self.script_path = self._load_model()
    print(obj.script_path, model_size, obj.model_size)
    if backend =="whisper":
        command =[ 
            obj.script_path,
            obj.input_path,
            obj.model_size,
            obj.language,
            obj.output_dir
        ]
        print("Running:", " ".join(command))

        result = subprocess.run(command, capture_output=True, text=True)

        print("✅ STDOUT:\n", result.stdout)
        if result.stderr:
            print("⚠️ STDERR:\n", result.stderr)

        return result.stdout
    else:
        obj.transcribeFastWhisper()
    










    # result = subprocess.run([obj.script_path], capture_output=True, text=True)
    
    # print("✅ Script output:")
    # print(result.stdout)