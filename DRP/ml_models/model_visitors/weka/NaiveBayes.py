from django.conf import settings
import uuid
from DRP.ml_models.model_visitors.weka.AbstractWekaModelVisitor import AbstractWekaModelVisitor
import os


class NaiveBayes(AbstractWekaModelVisitor):

    maxResponseCount = 1

    def __init__(self, *args, **kwargs):
        super(NaiveBayes, self).__init__(*args, **kwargs)


    def train(self, reactions, descriptorHeaders, filePath):
        arff_file = self._prepareArff(reactions, descriptorHeaders)

        # Currently, we support only one "response" variable.
        headers = [h for h in reactions.expandedCsvHeaders if h in descriptorHeaders]
        response_index = headers.index(list(self.statsModel.container.outcomeDescriptors)[0].csvHeader) + 1

        command = "java weka.classifiers.bayes.NaiveBayes -t {} -d {} -p 0 -c {}".format(arff_file, filePath, response_index)

        self._runWekaCommand(command)

    def wekaPredict(self, arff_file, model_file, response_index, results_path):
        command = "java weka.classifiers.bayes.NaiveBayes -T {} -l {} -p 0 -c {} 1> {}".format(arff_file, model_file, response_index, results_path)
        self._runWekaCommand(command)
        
    #def predict(self, reactions, descriptorHeaders):
        #arff_file = self._prepareArff(reactions, descriptorHeaders)
        #model_file = self.statsModel.fileName.name

        #results_file = "{}_{}.out".format(self.statsModel.pk, uuid.uuid4())
        #results_path = os.path.join(settings.TMP_DIR, results_file)

        ## Currently, we support only one "response" variable.
        #headers = [h for h in reactions.expandedCsvHeaders if h in descriptorHeaders]
        #response_index = headers.index(list(self.statsModel.container.outcomeDescriptors)[0].csvHeader) + 1

        ##TODO: Validate this input.
        #command = "java weka.classifiers.bayes.NaiveBayes -T {} -l {} -p 0 -c {} 1> {}".format(arff_file, model_file, response_index, results_path)
        #self._runWekaCommand(command)

        #response = list(self.statsModel.container.outcomeDescriptors)[0]
        #results = tuple((reaction, result) for reaction, result in zip(reactions, self._readWekaOutputFile(results_path)))
        #return {response :results}