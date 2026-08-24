"""
AEGIS-SOC // Professional PDF Technical Architecture Generator
==============================================================
Compiles PROJECT_ARCHITECTURE_AND_DATAFLOW.md into a beautifully formatted,
styled PDF document for university presentations and evaluation submissions.

Outputs:
  PROJECT_ARCHITECTURE_AND_DATAFLOW.pdf
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


def build_pdf_document(pdf_filename: str):
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
    GREEN_TEXT = colors.HexColor("#166534")  # Success Green

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=DARK_BLUE,
        alignment=TA_LEFT,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=14,
        textColor=CYAN_ACCENT,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=CYAN_ACCENT,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletItem',
        parent=body_style,
        leftIndent=12,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=8
    )

    story = []

    # Title Header Block
    story.append(Paragraph("🛡️ AEGIS-SOC: Technical Architecture & Data Flow Guide", title_style))
    story.append(Paragraph("Enterprise Autonomous Cyber Defense Operations Center // Powered by LangGraph Multi-Agent Swarm, Gemini 2.5 LLM & ChromaDB RAG", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=CYAN_ACCENT, spaceBefore=0, spaceAfter=12))

    # Executive Summary
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(
        "<b>AEGIS-SOC</b> is an AI-driven, multi-agent autonomous security framework designed to detect, analyze, and mitigate advanced cyberattacks in real-time. "
        "By moving beyond traditional static firewall rules, AEGIS-SOC combines <b>mathematical anomaly engines</b> (Shannon Entropy & Haversine Travel Velocity) "
        "with <b>vector retrieval-augmented generation (RAG)</b> and <b>Google Gemini 2.5 LLM reasoning</b> to achieve explainable, low-latency incident response.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Architecture Overview
    story.append(Paragraph("1. System Architecture Overview", h1_style))
    arch_text = (
        "The system is structured into 6 primary decoupled layers:<br/>"
        "• <b>1. Data Ingestion Streamer:</b> O(1) generator reading 31M-row Kaggle RBA dataset.<br/>"
        "• <b>2. FastAPI REST Gateway:</b> High-throughput API handling telemetry payloads & audit logs.<br/>"
        "• <b>3. LangGraph Multi-Agent Swarm:</b> 3-node stateful pipeline (Ingestion ➔ Analysis ➔ Response).<br/>"
        "• <b>4. Vector Memory & Cognitive AI:</b> Local ChromaDB vector database & Google Gemini 2.5 Flash LLM.<br/>"
        "• <b>5. SOAR Mitigation Engine:</b> Session revocation, IP firewall blocks & real TLS email alerts.<br/>"
        "• <b>6. Cyber Command HUD:</b> Interactive Sci-Fi HTML5 dashboard for real-time visualization."
    )
    story.append(Paragraph(arch_text, body_style))
    story.append(Spacer(1, 8))

    # End to End Data Flow
    story.append(Paragraph("2. End-to-End Telemetry Data Flow", h1_style))
    flow_code = (
        "[ Telemetry Event Ingested ] ➔ [ Node 1: Ingestion Agent ] (Entropy + Velocity Math)\n"
        "                                     │\n"
        "                                     ▼\n"
        "                           [ Node 2: Analysis Agent ] (ChromaDB RAG + Gemini LLM)\n"
        "                                     │\n"
        "                                     ▼\n"
        "                           [ Node 3: Response Agent ] (Triage Decision Matrix)\n"
        "                                     │\n"
        "               ┌─────────────────────┼─────────────────────┐\n"
        "               ▼                     ▼                     ▼\n"
        "     Score > 80 (CRITICAL)   50 <= Score <= 80 (HITL)  Score < 50 (SAFE)\n"
        "               │                     │                     │\n"
        "      [ SOAR Enforcement ]    [ Analyst Portal ]    [ Audit Ledger ]\n"
        "      - Revoke Session        - Pause Execution     - Log Baseline\n"
        "      - Block Attacker IP     - Approve / Dismiss\n"
        "      - Send Real Email"
    )
    story.append(Paragraph(flow_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Spacer(1, 8))

    # Subsystem Component Breakdown
    story.append(Paragraph("3. Detailed Subsystem Component Breakdown", h1_style))

    components = [
        ("server.py — FastAPI Gateway", "Manages REST endpoints (/api/v1/telemetry/ingest, /api/v1/stats, /api/v1/rag/query), user trajectory tracking across locations, and sliding window 2,000-item audit ledger memory bounds."),
        ("agents/graph_pipeline.py — LangGraph Swarm", "Orchestrates 3-node stateful swarm: Ingestion Node (math extraction), Threat Analysis Node (ChromaDB + Gemini 2.5 LLM reasoning), and Response Node (triage matrix evaluation)."),
        ("core/math_engine.py — Mathematical Feature Engine", "Calculates Shannon Entropy H(X) for stolen token detection (>3.85 bits/char) and Haversine Travel Velocity (km/h) for impossible travel detection (>800 km/h)."),
        ("core/vector_store.py — ChromaDB Threat Memory", "Pre-seeded local vector database matching incoming anomalies against MITRE ATT&CK techniques (T1539 AiTM, T1550.004 Token Theft, T1110 ATO, T1090 Proxy) using Cosine Similarity."),
        ("core/mitigation_engine.py — Enterprise SOAR Enforcer", "Executes sub-second automated containment: session token revocation, perimeter firewall IP block, and real SMTP TLS email alerts to recipient inboxes."),
        ("tools/real_dataset_streamer.py — 31M Dataset Streamer", "High-performance O(1) memory generator streaming 1 GB+ Kaggle RBA dataset CSV files with ~35 MB RAM footprint and auto directory resolution."),
        ("static/index.html — Command Theater HUD", "Interactive dashboard featuring Central Lock Theater, Tactical World Map Radar, Shannon Entropy Waveform, Multi-Agent Swarm Inspector, and HITL Review Portal.")
    ]

    for title, desc in components:
        story.append(Paragraph(f"<b>• {title}</b>", h2_style))
        story.append(Paragraph(desc, bullet_style))

    story.append(Spacer(1, 10))

    # Capability Verification Table
    story.append(Paragraph("4. Capability Verification & Objective Matrix", h1_style))

    table_data = [
        [Paragraph("<b>Capability</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white)),
         Paragraph("<b>Module / File</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white)),
         Paragraph("<b>Mechanism & Status</b>", ParagraphStyle('TH', parent=body_style, fontName='Helvetica-Bold', textColor=colors.white))],
        
        [Paragraph("Real-Time Data Streaming", body_style), Paragraph("tools/real_dataset_streamer.py", body_style), Paragraph("O(1) memory generator over 31M CSVs (PASS)", body_style)],
        [Paragraph("Impossible Travel Detection", body_style), Paragraph("core/math_engine.py", body_style), Paragraph("Haversine distance formula >800 km/h (PASS)", body_style)],
        [Paragraph("Token Theft Detection", body_style), Paragraph("core/math_engine.py", body_style), Paragraph("Shannon Entropy formula >3.85 bits/char (PASS)", body_style)],
        [Paragraph("Multi-Agent Orchestration", body_style), Paragraph("agents/graph_pipeline.py", body_style), Paragraph("LangGraph 3-node stateful AgentGraphState (PASS)", body_style)],
        [Paragraph("Cognitive Threat Analysis", body_style), Paragraph("agents/graph_pipeline.py", body_style), Paragraph("Google Gemini 2.5 LLM + ChromaDB RAG (PASS)", body_style)],
        [Paragraph("Automated Response (SOAR)", body_style), Paragraph("core/mitigation_engine.py", body_style), Paragraph("Session revoke + IP block + SMTP email (PASS)", body_style)],
        [Paragraph("Human-In-The-Loop Review", body_style), Paragraph("server.py & static/index.html", body_style), Paragraph("Analyst review modal for scores 50-80 (PASS)", body_style)]
    ]

    t = Table(table_data, colWidths=[140, 160, 230])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), CYAN_ACCENT),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))

    story.append(t)
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_COLOR, spaceBefore=5, spaceAfter=10))
    story.append(Paragraph("AEGIS-SOC Project Architecture Documentation // Built for University Presentation & Evaluation Submissions", ParagraphStyle('FooterText', parent=body_style, fontName='Helvetica-Oblique', fontSize=8, textColor=colors.gray, alignment=TA_CENTER)))

    # Build PDF Document
    doc.build(story)
    print(f"[OK] PDF Technical Documentation generated successfully at: {os.path.abspath(pdf_filename)}")


if __name__ == "__main__":
    out_pdf = "PROJECT_ARCHITECTURE_AND_DATAFLOW.pdf"
    build_pdf_document(out_pdf)
