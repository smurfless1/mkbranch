.PHONY: build
build: ./vendor ./mkbranch

.PHONY: ./mkbranch
./mkbranch:
	go build .

.PHONY: clean
clean:
	rm -rf ./vendor
	rm -f ./mkbranch

.PHONY: test
test:
	go test .

./vendor:
	go mod vendor

# GOSUMDB=off go get -u github.com/smurfless1/pathlib
#
