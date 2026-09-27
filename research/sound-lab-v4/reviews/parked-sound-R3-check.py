"""Independent DFT-block extraction and an out-of-model chirp challenge."""
from pathlib import Path
import hashlib
import importlib.util
import json
import wave
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def dft_extract(samples,fs=8000,n=64):
    x=np.asarray(samples,float)
    blocks=x[:len(x)//n*n].reshape(-1,n)
    transformed=np.fft.rfft(blocks,axis=1)
    amp=2*np.abs(transformed[:,[4,8]])/n
    times=(np.arange(len(blocks))*n+(n-1)/2)/fs
    selected=(times>=.05)&(times<=.95)
    centered=times[selected]-times[selected].mean()
    slopes=centered@np.log(amp[selected])/(centered@centered)
    return {"correctedAlpha_per_s":float(slopes[1]-slopes[0]),
            "targetSlope_per_s":float(slopes[0]),"referenceSlope_per_s":float(slopes[1]),
            "amplitudes":amp,"times":times}


def main():
    spec=importlib.util.spec_from_file_location("producer_r3",ROOT/"R3/run.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    files={}
    for path in sorted((ROOT/"R3").glob("*.wav")):
        with wave.open(str(path),"rb") as stream:
            assert stream.getnchannels()==1 and stream.getsampwidth()==2
            fs=stream.getframerate()
            y=np.frombuffer(stream.readframes(stream.getnframes()),dtype="<i2")/32767
        if "collision" in path.name:
            continue
        fit=dft_extract(y,fs)
        files[path.name]={k:v for k,v in fit.items() if k not in ["amplitudes","times"]}
        files[path.name]["sha256"]=hashlib.sha256(path.read_bytes()).hexdigest()
    assert files
    tau=(np.arange(64)-31.5)/8000
    def matrix(fr):
        return np.column_stack((np.cos(2*np.pi*500*tau),np.sin(2*np.pi*500*tau),
                                np.cos(2*np.pi*fr*tau),np.sin(2*np.pi*fr*tau)))
    designs={}
    for fr in [1000,500,505]:
        m=matrix(fr);rank=int(np.linalg.matrix_rank(m))
        designs[str(fr)]={"domainDimension":4,"rank":rank,"nullity":4-rank,
                          "condition":float(np.linalg.cond(m))}
    collision=matrix(500)
    kernels=[[1,0,-1,0],[0,1,0,-1]]
    residuals=[float(np.linalg.norm(collision@v)) for v in kernels]
    assert max(residuals)<1e-10 and designs["500"]["rank"]==2
    assert designs["505"]["condition"]>10 and designs["1000"]["rank"]==4
    # Model-mismatch attack: design stays full rank but the source frequency
    # sweeps 500→620 Hz. This is outside the frozen known-frequency model.
    t=np.arange(8000)/8000
    chirp=.2*np.exp(-2*t)*np.cos(2*np.pi*(500*t+60*t*t)+.3)
    reference=.05*np.exp(2*t)*np.cos(2*np.pi*1000*t+.7)
    pcm=np.round((chirp+reference)*32767).astype("<i2")
    decoded=pcm.astype(float)/32767
    independent=dft_extract(decoded)
    producer=module.extract_blocks(decoded)
    chirp_result={"trueAlpha_per_s":4,"targetFrequencyStart_Hz":500,
                  "targetFrequencyEnd_Hz":620,"independentCorrectedAlpha_per_s":independent["correctedAlpha_per_s"],
                  "independentAbsoluteError_per_s":abs(independent["correctedAlpha_per_s"]-4),
                  "interpretation":"A full-rank well-conditioned design cannot alone certify the assumed source frequencies or envelope model.",
                  "producerOutput":producer}
    # Convert producer NumPy data without hiding nonfinite values.
    def convert(value):
        if isinstance(value,np.ndarray):return value.tolist()
        if isinstance(value,np.generic):return value.item()
        if isinstance(value,dict):return {k:convert(v) for k,v in value.items()}
        if isinstance(value,(list,tuple)):return [convert(v) for v in value]
        return value
    result={"method":"Nominal DFT-bin projection independent of producer least squares; direct matrices and a chirp adversary.",
            "decodedFixtures":files,"independentDesigns":designs,"collisionKernels":kernels,
            "collisionKernelResiduals":residuals,"chirpAdversary":convert(chirp_result),
            "scriptSHA256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/"R3-independent-checks.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"decodedFixtures":files,"designs":designs,
                      "chirpAlpha_per_s":independent["correctedAlpha_per_s"]},indent=2))


if __name__=="__main__":main()
