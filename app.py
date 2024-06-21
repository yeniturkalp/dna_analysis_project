from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    dna_sequence = data['dna'].upper()
    
    # DNA Dizisi Kontrolü
    valid_bases = {'A', 'T', 'C', 'G'}
    invalid_indices = [i for i, base in enumerate(dna_sequence) if base not in valid_bases]
    
    if invalid_indices:
        return jsonify(
            error=f"Lütfen doğru DNA dizisi giriniz. Hatalı yerlerin indeks numaraları: {', '.join(map(str, invalid_indices))}"
        ), 400
    
    # GC Oranı Hesaplama
    gc_count = dna_sequence.count('G') + dna_sequence.count('C')
    gc_ratio = (gc_count / len(dna_sequence)) * 100
    
    # Tamamlayıcı Diziyi Oluşturma
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    complementary_sequence = ''.join([complement[base] for base in dna_sequence])
    
    return jsonify(gc_ratio=gc_ratio, complementary_sequence=complementary_sequence)

if __name__ == '__main__':
    app.run(debug=True)
