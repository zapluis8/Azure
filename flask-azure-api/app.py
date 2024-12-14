from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configurar conexión a MongoDB
app.config["MONGO_URI"] = "mongodb+srv://obatala:123@<cluster-url>/<nombre-base>"
mongo = PyMongo(app)

# Modelo de colección: estudiantes
coleccion_estudiantes = mongo.db.estudiantes

# Ruta raíz: renderiza HTML
@app.route("/")
def index():
    return render_template("index.html")

# Obtener todos los estudiantes (READ)
@app.route("/api/estudiantes", methods=["GET"])
def get_estudiantes():
    estudiantes = list(coleccion_estudiantes.find({}, {"_id": 0}))
    return jsonify(estudiantes)

# Agregar un estudiante (CREATE)
@app.route("/api/estudiantes", methods=["POST"])
def add_estudiante():
    nuevo_estudiante = request.json
    coleccion_estudiantes.insert_one(nuevo_estudiante)
    return jsonify({"mensaje": "Estudiante agregado"}), 201

# Actualizar un estudiante por nombre (UPDATE)
@app.route("/api/estudiantes/<string:nombre>", methods=["PUT"])
def update_estudiante(nombre):
    data = request.json
    resultado = coleccion_estudiantes.update_one({"nombre": nombre}, {"$set": data})
    if resultado.modified_count == 0:
        return jsonify({"error": "Estudiante no encontrado"}), 404
    return jsonify({"mensaje": "Estudiante actualizado"})

# Eliminar un estudiante por nombre (DELETE)
@app.route("/api/estudiantes/<string:nombre>", methods=["DELETE"])
def delete_estudiante(nombre):
    resultado = coleccion_estudiantes.delete_one({"nombre": nombre})
    if resultado.deleted_count == 0:
        return jsonify({"error": "Estudiante no encontrado"}), 404
    return jsonify({"mensaje": "Estudiante eliminado"})

if __name__ == "__main__":
    app.run(debug=True)
