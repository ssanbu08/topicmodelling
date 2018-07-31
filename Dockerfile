FROM continuumio/anaconda3
MAINTAINER Anbarasan ss.anbuselvan@gmail.com


# 1. RUN
RUN pip install -r requirements.txt
#RUN mkdir /opt/notebooks





# 2. Copy the Source code
COPY . /src

#3.CMD
CMD ['top']



# 3. Set the Entrypoint
# ENTRYPOINT [ “/bin/bash”, “-c” ]