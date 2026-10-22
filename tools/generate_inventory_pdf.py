"""
AEGIS-SOC // Technical Inventory PDF Compiler
=============================================
Compiles PROJECT_TECHNICAL_INVENTORY.md into a beautifully formatted,
styled PDF document for university presentations and project viva notes.

Outputs:
  PROJECT_TECHNICAL_INVENTORY.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT


def build_inventory_pdf(pdf_filename: str):
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0f172a")     # Dark Slate
    CYAN_ACCENT = colors.HexColor("#0284c7") # Ocean Blue
    DARK_BLUE = colors.HexColor("#1e293b")   # Header Text
    LIGHT_BG = colors.HexColor("#f8fafc")    # Box Background
    BORDER_COLOR = colors.HexColor("#cbd5e1")# Light Border
    PURPLE_ACCENT = colors.HexColor("#7c3aed")

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=DARK_BLUE,
        alignment=TA_LEFT,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10.5,
        leading=14,
        textColor=CYAN_ACCENT,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=CYAN_ACCENT,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletItem',
        parent=body_style,
        leftIndent=10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=5,
        spaceBefore=3,
        spaceAfter=6
    )

    story = []

    # Title Header Block
    story.append(Paragraph("🛡️ AEGIS-SOC: Master Technical Inventory", title_style))
    story.append(Paragraph("Complete Technical Reference of AI Models, Mathematical Algorithms, Datasets, MITRE TTPs & Technology Stacks", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=CYAN_ACCENT, spaceBefore=0, spaceAfter=10))

    # Section 1: AI Models
    story.append(Paragraph("1. AI & Machine Learning Models", h1_style))
    models_data = [
        [Paragraph("<b>Component</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white)),
         Paragraph("<b>Model / Engine</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white)),
         Paragraph("<b>Exact Function & Role</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white))],
        
        [Paragraph("Cognitive Threat Reasoner", body_style), Paragraph("Google Gemini 2.5 Flash<br/>(google-genai SDK)", body_style), Paragraph("Contextual behavioral reasoning, attacker intent inference, and Explainable AI (XAI) narrative generation.", body_style)],
        [Paragraph("Vector Embedding Model", body_style), Paragraph("all-MiniLM-L6-v2<br/>(ChromaDB Dense Embedder)", body_style), Paragraph("Converts MITRE ATT&CK tactics into 384-dimensional dense vectors for sub-millisecond semantic search.", body_style)]
    ]
    t1 = Table(models_data, colWidths=[130, 160, 240])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), CYAN_ACCENT),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t1)
    story.append(Spacer(1, 8))

    # Section 2: Mathematical Algorithms
    story.append(Paragraph("2. Core Mathematical Algorithms & Anomaly Formulas", h1_style))
    math_text = (
        "• <b>Shannon Information Entropy H(X):</b> Measures character randomness in session tokens.<br/>"
        "&nbsp;&nbsp;<i>Formula:</i> H(X) = - Σ P(x_i) log2 P(x_i). Tokens with entropy > 3.85 bits/char flag <b>MITRE T1550.004 (Token Theft)</b>.<br/>"
        "• <b>Haversine Travel Velocity Algorithm:</b> Computes great-circle geographic distance between consecutive logins.<br/>"
        "&nbsp;&nbsp;<i>Formula:</i> a = sin²(Δφ/2) + cos(φ1)cos(φ2)sin²(Δλ/2); v = distance / Δt. Speeds > 800 km/h flag <b>MITRE T1539 (AiTM Phishing)</b>.<br/>"
        "• <b>Cosine Distance Metric:</b> 1 - (u · v) / (||u|| ||v||) for sub-millisecond vector similarity search in ChromaDB.<br/>"
        "• <b>Sliding Window Array Bounding:</b> O(1) space cap keeping memory bounded under 50 MB RAM for 31M-row streams."
    )
    story.append(Paragraph(math_text, body_style))
    story.append(Spacer(1, 8))

    # Section 3: Multi-Agent Swarm
    story.append(Paragraph("3. LangGraph Stateful Multi-Agent Swarm", h1_style))
    swarm_data = [
        [Paragraph("<b>Agent Node</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white)),
         Paragraph("<b>Input State</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white)),
         Paragraph("<b>Function & Output State</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white))],
        
        [Paragraph("Node 1: Ingestion Agent", body_style), Paragraph("current_event, previous_event", body_style), Paragraph("Calculates Shannon Entropy, Haversine Velocity, checks VPN Proxy & Scanner User-Agents.", body_style)],
        [Paragraph("Node 2: Threat Analysis Agent", body_style), Paragraph("Math indicators, User context", body_style), Paragraph("Queries ChromaDB Vector RAG, prompts Gemini 2.5 Flash LLM, calculates risk score (0-100).", body_style)],
        [Paragraph("Node 3: Response Agent", body_style), Paragraph("Risk score, Classifications", body_style), Paragraph("Evaluates 3-Tier Triage: MONITOR (<50), HITL REVIEW (50-80), or CRITICAL BLOCK (>80).", body_style)]
    ]
    t2 = Table(swarm_data, colWidths=[130, 160, 240])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PURPLE_ACCENT),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t2)
    story.append(Spacer(1, 8))

    # Section 4: MITRE ATT&CK Matrix Mapping
    story.append(Paragraph("4. MITRE ATT&CK Enterprise Matrix Mapping", h1_style))
    mitre_data = [
        [Paragraph("<b>MITRE ID</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white)),
         Paragraph("<b>Technique Name</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white)),
         Paragraph("<b>Automated Detection Mechanism</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white))],
        
        [Paragraph("T1539", body_style), Paragraph("Adversary-in-the-Middle (AiTM)", body_style), Paragraph("Haversine Velocity > 800 km/h (Impossible Travel)", body_style)],
        [Paragraph("T1550.004", body_style), Paragraph("Pass-the-Cookie / Token Theft", body_style), Paragraph("Shannon Entropy > 3.85 bits/char (High Randomness)", body_style)],
        [Paragraph("T1110", body_style), Paragraph("Brute Force / Account Takeover", body_style), Paragraph("Automated Scanner User-Agents (Hydra / Nmap / urllib)", body_style)],
        [Paragraph("T1090", body_style), Paragraph("Proxy / Anonymizer Anomaly", body_style), Paragraph("Egress VPN headers & moderate velocity shifts", body_style)]
    ]
    t3 = Table(mitre_data, colWidths=[80, 200, 250])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t3)
    story.append(Spacer(1, 8))

    # Section 5: Real-World Dataset & Tech Stack
    story.append(Paragraph("5. Dataset & Full Technology Stack", h1_style))
    stack_text = (
        "• <b>Dataset:</b> Kaggle 31-Million Row Risk-Based Authentication (RBA) Dataset (462 MB, 31,269,266 rows).<br/>"
        "• <b>Backend Framework:</b> Python 3.11, FastAPI (v0.115+), Uvicorn ASGI Server, Pydantic v2.<br/>"
        "• <b>AI & Memory:</b> LangGraph (StateGraph), Google Gemini 2.5 Flash SDK, ChromaDB Vector Store.<br/>"
        "• <b>SOAR Mitigation:</b> Python smtplib (TLS Port 587 email dispatch), OAuth Session Revoker, IP Blacklister.<br/>"
        "• <b>Frontend HUD:</b> Tailwind CSS (Dark Mode), HTML5 Canvas/SVG, Google Orbitron & JetBrains Mono fonts.<br/>"
        "• <b>Testing Suite:</b> Python unittest (6 unit & integration tests, 100% pass rate in test_system.py)."
    )
    story.append(Paragraph(stack_text, body_style))
    story.append(Spacer(1, 10))

    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceBefore=5, spaceAfter=8))
    story.append(Paragraph("AEGIS-SOC Master Technical Inventory // Department of Computer Science & Engineering (Data Science)", ParagraphStyle('FooterText', parent=body_style, fontName='Helvetica-Oblique', fontSize=8, textColor=colors.gray, alignment=TA_CENTER)))

    doc.build(story)
    print(f"[OK] Master Technical Inventory PDF generated at: {os.path.abspath(pdf_filename)}")


if __name__ == "__main__":
    out_pdf = "PROJECT_TECHNICAL_INVENTORY.pdf"
    build_inventory_pdf(out_pdf)
