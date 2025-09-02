FROM ubuntu:24.04

RUN apt update -y
RUN apt upgrade -y

RUN apt install -y wget libgomp1 nano clustalw python3 python3-pip python3-numpy python3-tqdm

RUN wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.17.0+-x64-linux.tar.gz
RUN tar -xvf ncbi-blast-2.17.0+-x64-linux.tar.gz
RUN echo "export PATH=\$PATH:/ncbi-blast-2.17.0+/bin" >> ~/.bashrc

RUN mkdir /refseq
COPY other_scripts/DownloadFromFTP.py /refseq/download.py
RUN sh -c "cd /refseq/; python3 download.py"
RUN sh -c "cd /refseq/; gunzip *.gz"

RUN sh -c "cd /refseq/; wget https://s3ftp.flybase.org/genomes/Drosophila_melanogaster/dmel_r6.64_FB2025_03/fasta/dmel-all-transcript-r6.64.fasta.gz"
RUN sh -c "cd /refseq/; gunzip dmel-all-transcript-r6.64.fasta.gz"
RUN sh -c "cd /refseq/; mv dmel-all-transcript-r6.64.fasta fly.1.rna.fna"

RUN mkdir /padlock
COPY examples /padlock/examples
COPY lib /padlock/lib
COPY config.py /padlock/
COPY __init__.py /padlock/
COPY probedesign.py /padlock/

WORKDIR /padlock/