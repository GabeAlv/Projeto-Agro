#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <string>
#include <random>

// Função de Ativação ReLU e sua derivada
float relu(float x) { return std::max(0.0f, x); }
float relu_derivative(float x) { return x > 0.0f ? 1.0f : 0.0f; }

struct DataSample {
    std::vector<float> inputs;  // [timestamp, device_id, temp_ar, umid_solo, umid_ar]
    std::vector<float> targets; // [target_temp_ar, target_umid_solo, target_umid_ar]
};

struct Neuron {
    std::vector<float> weights;
    float bias;

    Neuron(int num_inputs) {
        bias = 0.01f;
        static std::default_random_engine generator(1337);
        // Inicialização de He / Xavier simplificada para estabilidade em redes profundas
        float stddev = std::sqrt(2.0f / num_inputs);
        std::normal_distribution<float> distribution(0.0f, stddev);
        for (int i = 0; i < num_inputs; ++i) {
            weights.push_back(distribution(generator));
        }
    }
};

class Layer {
public:
    int layer_id;
    std::vector<Neuron> neurons;
    std::vector<float> last_inputs;
    std::vector<float> last_raw_dots;
    std::vector<float> last_outputs;

    Layer(int id, int num_neurons, int inputs_per_neuron) : layer_id(id) {
        for (int i = 0; i < num_neurons; ++i) {
            neurons.push_back(Neuron(inputs_per_neuron));
        }
    }

    // Forward pass
    std::vector<float> forward(const std::vector<float>& inputs) {
        last_inputs = inputs;
        last_raw_dots.assign(neurons.size(), 0.0f);
        last_outputs.assign(neurons.size(), 0.0f);

        for (size_t n = 0; n < neurons.size(); ++n) {
            float dot = 0.0f;
            for (size_t i = 0; i < inputs.size(); ++i) {
                dot += neurons[n].weights[i] * inputs[i];
            }
            dot += neurons[n].bias;
            last_raw_dots[n] = dot;
            last_outputs[n] = relu(dot);
        }
        return last_outputs;
    }

    // Backward pass (Retorna o gradiente do erro em relação às entradas para a camada anterior)
    std::vector<float> backward(const std::vector<float>& output_gradients, float learning_rate) {
        std::vector<float> input_gradients(last_inputs.size(), 0.0f);

        for (size_t n = 0; n < neurons.size(); ++n) {
            // dL/dz = dL/da * da/dz
            float delta = output_gradients[n] * relu_derivative(last_raw_dots[n]);

            // Atualiza o gradiente que será passado para a camada anterior
            for (size_t i = 0; i < last_inputs.size(); ++i) {
                input_gradients[i] += delta * neurons[n].weights[i];
            }

            // Atualiza os pesos e bias do neurônio
            for (size_t i = 0; i < last_inputs.size(); ++i) {
                neurons[n].weights[i] -= learning_rate * delta * last_inputs[i];
            }
            neurons[n].bias -= learning_rate * delta;
        }

        return input_gradients;
    }

    // Exporta esta camada para um arquivo .h
    void export_to_header_file() const {
        std::string filename = "Camada_" + std::to_string(layer_id) + ".h";
        std::ofstream file(filename);

        file << "#ifndef CAMADA_" << layer_id << "_H\n";
        file << "#define CAMADA_" << layer_id << "_H\n\n";

        file << "// Configurações da Camada " << layer_id << "\n";
        file << "#define LAYER_ID " << layer_id << "\n";
        file << "#define NUM_NEURONS " << neurons.size() << "\n";
        file << "#define INPUTS_PER_NEURON " << (neurons.empty() ? 0 : neurons[0].weights.size()) << "\n\n";

        file << "const float PROGMEM WEIGHTS[NUM_NEURONS][INPUTS_PER_NEURON] = {\n";
        for (size_t i = 0; i < neurons.size(); ++i) {
            file << "    { ";
            for (size_t j = 0; j < neurons[i].weights.size(); ++j) {
                file << neurons[i].weights[j] << (j + 1 < neurons[i].weights.size() ? ", " : "");
            }
            file << " }" << (i + 1 < neurons.size() ? ",\n" : "\n");
        }
        file << "};\n\n";

        file << "const float PROGMEM BIASES[NUM_NEURONS] = {\n    ";
        for (size_t i = 0; i < neurons.size(); ++i) {
            file << neurons[i].bias << (i + 1 < neurons.size() ? ", " : "");
        }
        file << "\n};\n\n";

        file << "#endif\n";
        file.close();
    }
};

class Cortex {
public:
    std::vector<Layer> layers;

    Cortex(int total_layers, int input_dim, int hidden_dim, int output_dim) {
        // Camada 1: Entrada
        layers.push_back(Layer(1, hidden_dim, input_dim));

        // Camadas 2 a 39: Ocultas
        for (int i = 2; i < total_layers; ++i) {
            layers.push_back(Layer(i, hidden_dim, hidden_dim));
        }

        // Camada 40: Saída
        layers.push_back(Layer(total_layers, output_dim, hidden_dim));
    }

    std::vector<float> forward(const std::vector<float>& input) {
        std::vector<float> signal = input;
        for (auto& layer : layers) {
            signal = layer.forward(signal);
        }
        return signal;
    }

    void train(const std::vector<DataSample>& dataset, int epochs, float learning_rate) {
        for (int epoch = 1; epoch <= epochs; ++epoch) {
            float total_loss = 0.0f;

            for (const auto& sample : dataset) {
                // 1. Forward Pass
                std::vector<float> predictions = forward(sample.inputs);

                // 2. Cálculo do Erro / Gradiente na Camada de Saída (Erro Quadrático Médio)
                std::vector<float> output_gradients(predictions.size());
                for (size_t i = 0; i < predictions.size(); ++i) {
                    float error = predictions[i] - sample.targets[i];
                    output_gradients[i] = error; // dL/dOut
                    total_loss += error * error;
                }

                // 3. Backpropagation através das 40 camadas (de trás para frente)
                std::vector<float> current_gradients = output_gradients;
                for (int l = (int)layers.size() - 1; l >= 0; --l) {
                    current_gradients = layers[l].backward(current_gradients, learning_rate);
                }
            }

            if (epoch % 10 == 0 || epoch == epochs) {
                std::cout << "Época " << epoch << "/" << epochs 
                          << " - Perda Média (Loss): " << (total_loss / dataset.size()) << "\n";
            }
        }
    }

    void export_all() const {
        for (const auto& layer : layers) {
            layer.export_to_header_file();
        }
    }
};

// Carregador de arquivo CSV
std::vector<DataSample> load_csv(const std::string& filepath) {
    std::vector<DataSample> dataset;
    std::ifstream file(filepath);

    if (!file.is_open()) {
        std::cerr << "Erro ao abrir o arquivo: " << filepath << "\n";
        return dataset;
    }

    std::string line;
    bool is_header = true;

    while (std::getline(file, line)) {
        if (line.empty()) continue;
        if (is_header) { is_header = false; continue; } // Pula o cabeçalho

        std::stringstream ss(line);
        std::string value;
        std::vector<float> row;

        while (std::getline(ss, value, ',')) {
            row.push_back(std::stof(value));
        }

        // Verifica se a linha contém as 5 entradas + 3 saídas esperadas
        if (row.size() >= 8) {
            DataSample sample;
            sample.inputs  = {row[0], row[1], row[2], row[3], row[4]};
            sample.targets = {row[5], row[6], row[7]};
            dataset.push_back(sample);
        }
    }

    file.close();
    return dataset;
}

int main() {
    std::string csv_file = "dados_treino.csv";
    std::cout << "Carregando dataset de '" << csv_file << "'...\n";
    
    std::vector<DataSample> dataset = load_csv(csv_file);

    if (dataset.empty()) {
        std::cerr << "Nenhum dado válido carregado. Encerrando programa.\n";
        return 1;
    }

    std::cout << "Dataset carregado com " << dataset.size() << " amostras.\n";

    // Configuração da Rede Multicamadas (40 Camadas)
    const int TOTAL_LAYERS = 40;
    const int INPUT_SIZE  = 5;
    const int HIDDEN_SIZE = 16;
    const int OUTPUT_SIZE = 3;

    Cortex cortex(TOTAL_LAYERS, INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE);

    std::cout << "\nIniciando treinamento da rede de 40 camadas...\n";
    cortex.train(dataset, 100, 0.001f); // 100 Épocas com Learning Rate = 0.001

    std::cout << "\nTreinamento concluído. Exportando arquivos .h de cada camada...\n";
    cortex.export_all();
    std::cout << "Finalizado com sucesso! 40 arquivos (Camada_1.h a Camada_40.h) foram salvos.\n";

    return 0;
}
