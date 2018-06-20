import wave
import struct
import math
import os
from scipy import fromstring, int16

# 一応既に同じ名前のディレクトリがないか確認。
file = os.path.exists("output")
print(file)

if file == False:
    #保存先のディレクトリの作成
    os.mkdir("output")

def cut_wav(filename,time,start):  # WAVファイルを刈り奪る　形をしてるだろ？ 
    # timeの単位は[sec]

    # ファイルを読み出し
    wavf = str(filename) + '.wav'
    wr = wave.open(wavf, 'r')

    # waveファイルが持つ性質を取得
    ch = wr.getnchannels()
    width = wr.getsampwidth()
    fr = wr.getframerate()
    fn = wr.getnframes()
    total_time = 1.0 * fn / fr
    integer = math.floor(total_time) # 小数点以下切り捨て
    t = int(time)  # 秒数[sec]
    frames = int(ch * fr * t)
    num_cut = int(integer//t)

    #　確認用
#     print("Channel: ", ch)
#     print("Sample width: ", width)
#     print("Frame Rate: ", fr)
    print("Frame num: ", fn)
#     print("Params: ", wr.getparams())
    print("Total time: ", total_time ,"sec")
#     print("Total time(integer)",integer)
#     print("Time: ", t) 
#     print("Frames: ", frames) 
    print("Number of cut: ",num_cut)

    # waveの実データを取得し、数値化
    data = wr.readframes(wr.getnframes())
    wr.close()
    X = fromstring(data, dtype=int16)
#     print(X)


    for i in range(num_cut):
#         print(i)
        # 出力データを生成
        outf = 'output/' + str(i+start) + '.wav' 
        start_cut = i*frames
        end_cut = i*frames + frames
#         print(start_cut)
#         print(end_cut)
        Y = X[start_cut:end_cut]
        outd = struct.pack("h" * len(Y), *Y)

        # 書き出し
        ww = wave.open(outf, 'w')
        ww.setnchannels(ch)
        ww.setsampwidth(width)
        ww.setframerate(fr)
        ww.writeframes(outd)
        ww.close()
        
    return i+start+1 #　現在のカット済のファイル名の次を返す（はず）

n = 0
print("cut time = ")
cut_time = input()
print("Number of file = ")
a = input()
num_file = int(a)+1
print('=====================================================')
for name_file in range(int(num_file)):
    print("name_file : ",name_file,".wav")
    n = cut_wav(name_file,cut_time,n)
    print('return :',n)
    print('=====================================================')
