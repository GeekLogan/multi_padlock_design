from ftplib import FTP
import os
import tqdm

# connect to NCBI FTP server
ftp = FTP('ftp.ncbi.nlm.nih.gov')
ftp.login()     # anonymous login

# move to refseq directory
#ftp.cwd('refseq')

# list contents
#ftp.retrlines('LIST')

for organism in ['H_sapiens', 'M_musculus']:
    print(f'Downloading for {organism}...')
    
    # move to species specific subdirectory
    ftp.cwd(f'/refseq/{organism}/mRNA_Prot')
    allfiles = ftp.nlst()

    allfiles = [x for x in allfiles if 'rna.fna' in x]

    for file in tqdm.tqdm(allfiles):
        #if 'rna.fna' in file:
        #ftp.retrbinary('RETR ' + file,
        #               open(os.path.join('F:\ProbeDesign\RefSeqDatabase', file), 'wb').write)
        print(file)

        with open(f'./{file}', 'wb') as f:
            ftp.retrbinary(f'RETR {file}', f.write)

ftp.quit()