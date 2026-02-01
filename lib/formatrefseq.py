# for multi_padlock_design
# Xiaoyan, 2017

import os
import config
import gzip


def fastadb(indir, filenum, filename, name):
    """Read multiple fasta files of a database, prepare acronyms (NCBI only), and format database for blast"""
    # read original .fna files
    Headers = []
    Seq = []
    seq = str()

    for i in range(filenum):
        digit = str(i + 1)

        with open(
            os.path.join(indir, filename[0] + digit + filename[1]),
            "r",
        ) as f:
            print(digit)

            for line in f:
                line = line.strip()
                if line:
                    if line[0] == ">":  # a new sequence
                        if len(Headers):  # not the first sequence
                            Seq.append([seq])
                        Headers.append(line)
                        seq = str()
                    else:
                        seq += line

    Seq.append(seq)  # the last sequence

    # write all entries to file
    with open(os.path.join(indir, name + ".allheaders.txt"), "w") as f:
        with open(os.path.join(indir, name + ".allseqs.txt"), "w") as fs:
            for c, gene in enumerate(Headers):
                f.write("%s\n" % gene)
                fs.write("%s\n" % Seq[c][0])

    if 'fly' not in filename[0]:  # fly database already filtered
        # retain only NM and NR entries
        for c in range(len(Headers) - 1, -1, -1):
            if "|" in Headers[c]:
                header = Headers[c].split("|")
                if len(header) <= 3:
                    if not (
                        header[1][:2] == "NM" or header[1][:2] == "NR"
                    ):  # new NCBI fna format
                        del Headers[c]
                        del Seq[c]
                else:
                    if not (
                        header[3][:2] == "NM" or header[3][:2] == "NR"
                    ):  # old NCBI fna format
                        del Headers[c]
                        del Seq[c]
            else:
                if not (
                    Headers[c][1:3] == "NM" or Headers[c][1:3] == "NR"
                ):  # new NCBI single fasta file format
                    del Headers[c]
                    del Seq[c]

    # write selected sequences to file
    with open(os.path.join(indir, name + ".selectedheaders.txt"), "w") as f:
        with open(os.path.join(indir, name + ".selectedseqs.txt"), "w") as fs:
            for c, gene in enumerate(Headers):
                if 'fly' in filename[0]:
                    genename = gene.split(" parent=")[1].split(";")[0]
                    f.write(f"{gene.split()[0]}\n")
                    fs.write(f"{Seq[c][0]}\n")
                else:
                    f.write(f"{gene}\n")
                    fs.write(f"{Seq[c][0]}\n")

    # acronyms only
    HeadersAcronym = []
    if 'fly' in filename[0]:  # fly database
        for header in Headers:
            genename = header.split(" parent=")[1].split(";")[0]
            HeadersAcronym.append(genename)
    else:
        for header in Headers:
            par1 = header.split("(")
            par2 = header.split(")")
            if len(par1) == 2:
                HeadersAcronym.append(par2[0][len(par1[0]) - len(par2[0]) + 1 :])
            else:
                HeadersAcronym.append(par2[-2][-len(par1[-1]) + len(par2[-1]) + 1 :])

    # write acronyms to file
    with open(os.path.join(indir, name + ".acronymheaders.txt"), "w") as f:
        for c, gene in enumerate(HeadersAcronym):
            f.write("%s\n" % gene)


def blastdb(species):
    """Format fasta sequences to BLAST database"""
    fastadir = (config.fastadir_mouse, config.fastadir_human, config.fastadir_fly)
    nfiles = (config.fasta_filenum_mouse, config.fasta_filenum_human, config.fasta_filenum_fly)
    filename = (config.fasta_pre_suffix_mouose, config.fasta_pre_suffix_human, config.fasta_pre_suffix_fly)

    if species == "mouse":
        s = 0
    elif species == "human":
        s = 1
    elif species == "fly":
        s = 2

    if not os.path.isfile(os.path.join(fastadir[s], species + ".transcriptome.nal")):
        try:
            alldb = []
            # make database file from fna
            for i in range(nfiles[s]):
                digit = str(i + 1)
                txtcmd = " ".join(
                    (
                        "makeblastdb -in",
                        os.path.join(
                            fastadir[s],
                            filename[s][0] + digit + filename[s][1].replace(".gz", ""),
                        ),
                        "-dbtype nucl",
                    )
                )
                os.system(txtcmd)
                alldb.append(
                    os.path.join(
                        fastadir[s], filename[s][0] + digit + filename[s][1]
                    ).replace(".gz", "")
                )

            # aggregate databases
            alldb = " ".join(tuple(alldb))
            txtcmd = " ".join(
                (
                    "blastdb_aliastool -dblist",
                    '"' + alldb + '"',
                    "-dbtype nucl",
                    "-out " + os.path.join(fastadir[s], species + ".transcriptome"),
                    "-title " + '"' + species + "_transcriptome" + '"',
                )
            )
            os.system(txtcmd)

        except:
            print(" Could not format BLAST database")
