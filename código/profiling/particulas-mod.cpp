#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <filesystem>


int _proc_file(const std::string& filepath, double center_x, double center_y, double radius) {
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



static PyObject *
proc_file(PyObject *self, PyObject *args, PyObject *kwargs)
{
    const char *filepath;
    double center_x, center_y, radius;
    int count;

    const char *kwlist[] = {"filepath", "center_x", "center_y", "radius", NULL};

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs, "sddd", const_cast<char **>(kwlist), 
            &filepath, &center_x, &center_y, &radius))
        return NULL;

    count = _proc_file(filepath, center_x, center_y, radius);

    return PyLong_FromLong(count);
}


static PyMethodDef ProcFileMethods[] = {
    {"proc_file", (PyCFunction)proc_file, METH_VARARGS | METH_KEYWORDS, "Process a file."},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef particulasmodule = {
    PyModuleDef_HEAD_INIT,
    "particulas_mod_7",
    NULL,
    -1, 
    ProcFileMethods
};


PyMODINIT_FUNC
PyInit_particulas_mod_7(void)
{
    return PyModule_Create(&particulasmodule);
}

// Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
// Licencia CC BY-NC-SA 4.0
// Para más info visitar https://github.com/facundobatista/libro-pyciencia/
