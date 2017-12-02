DK=docker
CNAME=kiva
IMG=kiva

build:
	$(DK) build . -t $(IMG)

test:
	$(DK) run --name $(CNAME) $(IMG)

bash:
	$(DK) run --name $(CNAME) -it $(IMG) bash

rm:
	$(DK) rm $(CNAME)

rmi:
	$(DK) rmi $(IMG) -f
