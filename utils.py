from fpdf import FPDF
import io
import pandas as pd

def convert_text_to_pdf(text):
    """
    Convertit du texte en PDF avec gestion d'erreurs et encodage
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Essayer d'ajouter une police qui supporte l'UTF-8
        try:
            pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
            pdf.set_font('DejaVu', size=11)
        except:
            # Fallback vers Arial si DejaVu n'est pas disponible
            pdf.set_font("Arial", size=11)
        
        # Nettoyer le texte pour éviter les caractères problématiques
        clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
        
        # Ajouter le contenu ligne par ligne
        for line in clean_text.split('\n'):
            if line.strip():  # Ignorer les lignes vides
                try:
                    pdf.multi_cell(0, 8, line.strip())
                    pdf.ln(2)  # Petit espacement
                except:
                    # Si une ligne pose problème, l'ignorer
                    continue
        
        # Créer le buffer
        buffer = io.BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin-1')
        buffer.write(pdf_output)
        buffer.seek(0)
        
        return buffer
        
    except Exception as e:
        raise Exception(f"Erreur lors de la création du PDF: {str(e)}")

def convert_text_to_csv(text):
    """
    Convertit du texte en CSV avec structure améliorée
    """
    try:
        # Diviser le texte en sections logiques
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Créer un DataFrame structuré
        data = {
            "Section": [],
            "Contenu": []
        }
        
        current_section = "Introduction"
        for line in lines:
            # Détecter les titres (commencent par # ou sont en majuscules)
            if line.startswith('#') or (len(line) < 50 and line.isupper()):
                current_section = line.replace('#', '').strip()
            else:
                data["Section"].append(current_section)
                data["Contenu"].append(line)
        
        # Si pas de structure détectée, format simple
        if not data["Section"]:
            data = {"Résumé": lines}
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False, encoding='utf-8-sig')  # utf-8-sig pour Excel
        
    except Exception as e:
        # Fallback simple en cas d'erreur
        simple_data = {"Résumé": [text]}
        df = pd.DataFrame(simple_data)
        return df.to_csv(index=False, encoding='utf-8-sig')