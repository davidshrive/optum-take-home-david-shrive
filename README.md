# optum-take-home-david-shrive

# Notes
Due to existing commitments for this week I was only able to spend a few hours on this take home and as Jay has already checked in once I figured I'd best hand it in ASAP. 

Within this time I was able to map the Patient type resource using a combination of specific functions (for name, adddress, telecom objects) as well as a more general function for the extension objects that are used in a variety of places. The patient information for all provided input files is mapped and then output into a single [csv file](output/patients.csv). I also added a basic [test suite](tests) and a [dockerised](Dockerfile) my work.


# Future Improvements
* The test suite could definetly be added too, I've barely scratched the surface.
* I did find a python [library](https://pypi.org/project/fhir.resources/) for working with the FHIR data format but decided against using it as I thought the manual approach would enable you to evaluate my coding ability better, however, in hindsight, I suspect this may have been a better approach.

# Run
`python script.py`

And the tests can be ran via...

`pytest`

# Docker
## Build
`sudo docker image build -t optum-takehome .`

## Run
`sudo docker run  -v ./input:/input -v ./output:/output optum-takehome`