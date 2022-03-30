from __future__ import print_function
import os
import subprocess
from subprocess import PIPE
import shutil
#brew install ghostscript
if __name__ == '__main__':
    PATH_GS='/usr/local/bin/gs'
    path_source=''
    path_destination = os.path.join(path_source,'out')
    sizeMaxInByte=1000000 #(1Mb)
    if not os.path.isdir(path_destination):
        os.mkdir(path_destination)
    path, dirs, filesCount = next(os.walk(path_source))
    file_count = len(filesCount)
    i=1
    for entry in os.scandir(path_source):
        filename = entry.name
        fileinput = path_source + entry.name
        if entry.is_file() and  ('pdf' in filename) and os.path.getsize(fileinput)>sizeMaxInByte:
                i=i+1
    print('SARANNO ELABORATI : '+  '' + str(i) + '  files su ' + str( file_count) + '')
    i = 1
    for entry in os.scandir(path_source):
        filename = entry.name
        fileinput = path_source + entry.name
        output_file = str(path_destination) + '/' + filename
        if entry.is_file() or  ('pdf' in filename):
                if os.path.getsize(fileinput)>sizeMaxInByte:
                    print('Elaboro -> '+filename +'   | '+str(int((i/file_count)*100))+'%')
                    print('     Dimensione Iniziale (byte):  '+ str(os.path.getsize(fileinput)))
                    #print(output_file)
                    p = subprocess.Popen(
                        [ PATH_GS, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                         '-sColorConversionStrategy=Gray', '-sProcessColorModel=DeviceGray',
                         '-dColorImageResolution=72','-dNOPAUSE', '-dBATCH','-dPDFSETTINGS=/ebook', '-dQUIET', '-o',
                         output_file, fileinput], stdin=PIPE, stdout=PIPE ,stderr=PIPE)
                    output, error =p.communicate()
                    if p.returncode != 0:
                        print("elaboration failed %d %s %s" % (p.returncode, output, error))
                    print('     Dimensione Finale (byte):    '+ str(os.path.getsize(output_file)))
                else:
                    print("Non elaboro il file - copio: ",output_file)
                    p = subprocess.call('cp '+str(fileinput)+'  '+str(output_file),shell=True)
        i = i + 1
    path, dirs, filesCountFinal = next(os.walk(path_destination))
    print('INIZIALE :',len(filesCount),'   - FINALE:  ',len((filesCountFinal)))


