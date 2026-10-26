FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /work

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    latexmk \
    lmodern \
    fonts-urw-base35 \
    texlive-luatex \
    texlive-fonts-extra \
    texlive-latex-extra \
    texlive-pictures \
    texlive-plain-generic \
 && rm -rf /var/lib/apt/lists/*

COPY . /work

RUN git clone https://github.com/rpgtex/DND-5e-LaTeX-Template /tmp/DND-5e-LaTeX-Template \
 && git -C /tmp/DND-5e-LaTeX-Template checkout 2c94ab97952b8285bbbc932ccd507cbcd931ef82 \
 && mkdir -p /work/.cache /work/template/fonts

ENV TEXINPUTS=/work//:/tmp/DND-5e-LaTeX-Template//:
ENV TTFONTS=/work//:/tmp/DND-5e-LaTeX-Template//:
ENV TEXMFHOME=/work/.cache
ENV TEXMFVAR=/work/.cache/texmf-var

COPY docker/render /usr/local/bin/render
RUN chmod +x /usr/local/bin/render

ENTRYPOINT ["render"]

