#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <filesystem>


int proc_file(const std::string& filepath, double center_x, double center_y, double radius) {
    int count = 0;
    double particle_x, particle_y, particle_radius;
    std::string raw_line;

    // abrimos el archivo
    std::ifstream srcfile(filepath);
    if (!srcfile.is_open()) {
        std::cerr << "Error opening file: " << filepath << std::endl;
        exit(1);
    }

    while (std::getline(srcfile, raw_line)) {
        std::istringstream stream_line(raw_line);

        // separamos por coma
        std::vector<std::string> raw_values;
        while(stream_line.good())
        {
            std::string substr;
            getline(stream_line, substr, ',');
            raw_values.push_back(substr);
        }
        if (raw_values.size() != 3) {
            std::cerr << "Error parsing line: " << raw_line << std::endl;
            exit(1);
        }

        // convertimos los valores a double
        particle_x = std::stod(raw_values[0]);
        particle_y = std::stod(raw_values[1]);
        particle_radius = std::stod(raw_values[2]);

        // evaluamos y contamos si corresponde
        double dist_centers = std::pow(particle_x - center_x, 2) + std::pow(particle_y - center_y, 2);
        if (dist_centers <= std::pow(radius + particle_radius, 2)) {
            count++;
        }
    }
    srcfile.close();
    return count;
}


int main(int argc, char** argv) {
    if (argc != 6) {
        std::cerr << "Usage: " << argv[0] << " <dirpath> <results_file> <center_x> <center_y> <radius>" << std::endl;
        return 1;
    }

    std::string basedir = argv[1];
    std::string results_file = argv[2];
    double center_x = std::stod(argv[3]);
    double center_y = std::stod(argv[4]);
    double radius = std::stod(argv[5]);

    // abrimos el archivo de salida
    std::ofstream outfh(results_file);
    if (!outfh.is_open()) {
        std::cerr << "Error opening output file: " << results_file << std::endl;
        return 1;
    }

    // recorremos el árbol de directorios y parseamos cada archivo
    for (const auto& entry : std::filesystem::recursive_directory_iterator(basedir)) {
        if (entry.is_regular_file()) {
            int count = proc_file(entry.path().string(), center_x, center_y, radius);
            outfh << entry.path().filename().string() << "," << count << "\n";
        }
    }

    outfh.close();
    return 0;
}

// Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
// Licencia CC BY-NC-SA 4.0
// Para más info visitar https://github.com/facundobatista/libro-pyciencia/
