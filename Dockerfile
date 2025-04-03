FROM ubuntu:24.04

RUN apt update -y
RUN apt upgrade -y

RUN apt install -y wget libgomp1 nano clustalw python3 python3-pip python3-numpy python3-tqdm

RUN wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.16.0+-x64-linux.tar.gz
RUN tar -xvf ncbi-blast-2.16.0+-x64-linux.tar.gz
RUN echo "export PATH=\$PATH:/ncbi-blast-2.16.0+/bin" >> ~/.bashrc

RUN mkdir /padlock
COPY examples /padlock/examples
COPY lib /padlock/lib
COPY config.py /padlock/
COPY __init__.py /padlock/
COPY probedesign.py /padlock/

RUN mkdir /refseq
COPY other_scripts/DownloadFromFTP.py /refseq/download.py
RUN sh -c "cd /refseq/; python3 download.py"
RUN sh -c "cd /refseq/; gunzip *.gz"

WORKDIR /padlock/