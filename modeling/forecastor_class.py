class Predictor:

  def __init__(self, name, data, parameters):
    self.name = name
    self.data = data
    self.parameters = parameters

  def atributes(self):
    print(self.name, ":", sep="")
    print("Parameters:", self.parameters)

  def train_model(self, fuerza, inteligencia, defensa):
    

  def predict(self):
    return self.vida > 0

  def error_metrics(self):
    