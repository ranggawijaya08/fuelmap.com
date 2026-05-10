import googlemaps
from flask import Flask, request, jsonify

app = Flask(__name__)


API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'
gmaps = googlemaps.Client(key=API_KEY)

@app.route('/hitung-biaya', methods=['POST'])
def hitung_biaya():
    data = request.json

    try:
        
        lat1 = data.get('latAwal')
        lon1 = data.get('longAwal')
        lat2 = data.get('latTujuan')
        lon2 = data.get('longTujuan')
        
        
        konsumsi = float(data.get('konsumsi', 40)) 
        
        harga_per_liter = float(data.get('harga_bbm', 0))

        
        origin = (lat1, lon1)
        destination = (lat2, lon2)
        
        directions_result = gmaps.directions(
            origin,
            destination,
            mode="driving"
        )

        if not directions_result:
            return jsonify({"status": "error", "message": "Rute tidak ditemukan"}), 404

        
        jarak_meter = directions_result[0]['legs'][0]['distance']['value']
        jarak_km = jarak_meter / 1000

        if konsumsi <= 0:
            return jsonify({"error": "Konsumsi BBM harus lebih dari 0"}), 400

        
        liter_dibutuhkan = jarak_km / konsumsi
        total_biaya = liter_dibutuhkan * harga_per_liter

        return jsonify({
            "status": "success",
            "hasil": {
                "jarak_km": round(jarak_km, 2),
                "bbm_liter": round(liter_dibutuhkan, 2),
                "total_biaya": int(total_biaya)
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    
    app.run(debug=True, port=5000)