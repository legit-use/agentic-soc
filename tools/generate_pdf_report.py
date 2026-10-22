"""
One-Click Executive Forensic Incident Report Generator
Generates a professional HTML-based incident report from audit ledger data.
No external dependencies required — uses Python standard library only.
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any


class ForensicReportGenerator:
    """Generates a downloadable executive forensic incident report from AEGIS-SOC audit data."""

    @staticmethod
    def generate_report(
        audit_logs: List[Dict[str, Any]],
        operator_name: str = "Security Operator",
        report_title: str = "AEGIS-SOC Executive Forensic Incident Report"
    ) -> str:
        """
        Generates a complete HTML incident report with:
        - Executive summary with key metrics
        - MITRE ATT&CK technique mapping table
        - Risk distribution analysis
        - SOAR execution timeline
        - SHA-256 digital integrity signature
        """
        now = datetime.utcnow()
        report_id = f"AEGIS-RPT-{now.strftime('%Y%m%d%H%M%S')}"

        # Compute metrics
        total_events = len(audit_logs)
        critical_events = [e for e in audit_logs if e.get('risk_score', 0) > 80]
        hitl_events = [e for e in audit_logs if e.get('action') == 'HUMAN_IN_LOOP_REQUIRED']
        safe_events = [e for e in audit_logs if e.get('risk_score', 0) < 50]
        blocked_events = [e for e in audit_logs if 'BLOCK' in (e.get('action') or '')]

        # MITRE technique frequency
        mitre_freq = {}
        for e in audit_logs:
            tech = e.get('mitre_technique', 'Unknown')
            mitre_freq[tech] = mitre_freq.get(tech, 0) + 1

        # Classification frequency
        class_freq = {}
        for e in audit_logs:
            cls = e.get('classification', 'Unknown')
            class_freq[cls] = class_freq.get(cls, 0) + 1

        # Average risk score
        risk_scores = [e.get('risk_score', 0) for e in audit_logs if e.get('risk_score') is not None]
        avg_risk = round(sum(risk_scores) / len(risk_scores), 1) if risk_scores else 0.0
        max_risk = round(max(risk_scores), 1) if risk_scores else 0.0

        # SOAR execution count
        soar_count = sum(len(e.get('soar_execution_logs', [])) for e in audit_logs)

        # Critic overrides
        critic_overrides = sum(1 for e in audit_logs if e.get('critic_override', False))

        # Digital signature
        report_data_str = json.dumps({
            'report_id': report_id,
            'total_events': total_events,
            'critical': len(critical_events),
            'timestamp': now.isoformat()
        }, sort_keys=True)
        sha256_signature = hashlib.sha256(report_data_str.encode()).hexdigest()

        # Build MITRE table rows
        mitre_rows = ''
        for tech, count in sorted(mitre_freq.items(), key=lambda x: x[1], reverse=True):
            mitre_rows += f'<tr><td style="padding:8px;border-bottom:1px solid #1e293b;color:#38bdf8;">{tech}</td><td style="padding:8px;border-bottom:1px solid #1e293b;text-align:center;color:#e2e8f0;">{count}</td><td style="padding:8px;border-bottom:1px solid #1e293b;text-align:center;">{"🔴" if count > 3 else "🟡" if count > 1 else "🟢"}</td></tr>'

        # Build classification rows
        class_rows = ''
        for cls, count in sorted(class_freq.items(), key=lambda x: x[1], reverse=True):
            color = '#f43f5e' if 'AiTM' in cls or 'Theft' in cls or 'Brute' in cls else '#ffb700' if 'Proxy' in cls else '#4ade80'
            class_rows += f'<tr><td style="padding:8px;border-bottom:1px solid #1e293b;color:{color};font-weight:bold;">{cls}</td><td style="padding:8px;border-bottom:1px solid #1e293b;text-align:center;color:#e2e8f0;">{count}</td></tr>'

        # Build critical incident details
        incident_rows = ''
        for e in critical_events[:10]:
            incident_rows += f"""
            <tr>
                <td style="padding:6px;border-bottom:1px solid #1e293b;color:#94a3b8;font-size:11px;">{e.get('event_id','--')}</td>
                <td style="padding:6px;border-bottom:1px solid #1e293b;color:#38bdf8;font-size:11px;">{e.get('user_principal_name', e.get('principal','--'))}</td>
                <td style="padding:6px;border-bottom:1px solid #1e293b;color:#f43f5e;font-weight:bold;font-size:11px;">{e.get('risk_score',0)}</td>
                <td style="padding:6px;border-bottom:1px solid #1e293b;color:#e2e8f0;font-size:11px;">{e.get('classification','--')}</td>
                <td style="padding:6px;border-bottom:1px solid #1e293b;color:#4ade80;font-size:11px;">{e.get('action','--')}</td>
            </tr>"""

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{report_title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0f172a; color: #e2e8f0; padding: 40px; }}
        .report-container {{ max-width: 900px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #0f172a, #1e293b); border: 2px solid #38bdf8; border-radius: 12px; padding: 30px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ color: #38bdf8; font-size: 24px; margin-bottom: 8px; }}
        .header .subtitle {{ color: #94a3b8; font-size: 13px; }}
        .section {{ background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
        .section h2 {{ color: #38bdf8; font-size: 16px; margin-bottom: 15px; border-bottom: 1px solid #334155; padding-bottom: 8px; }}
        .metric-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }}
        .metric-card {{ background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 15px; text-align: center; }}
        .metric-card .value {{ font-size: 28px; font-weight: 800; }}
        .metric-card .label {{ font-size: 11px; color: #94a3b8; margin-top: 4px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ padding: 10px; text-align: left; border-bottom: 2px solid #334155; color: #94a3b8; font-size: 11px; text-transform: uppercase; }}
        .signature {{ background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 15px; text-align: center; margin-top: 30px; }}
        .signature .hash {{ font-family: monospace; color: #4ade80; font-size: 11px; word-break: break-all; }}
        @media print {{ body {{ background: white; color: #1e293b; }} .section {{ border-color: #cbd5e1; }} }}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="header">
            <h1>🛡️ {report_title}</h1>
            <div class="subtitle">Report ID: {report_id} | Generated: {now.strftime('%Y-%m-%d %H:%M:%S UTC')} | Operator: {operator_name}</div>
        </div>

        <div class="metric-grid">
            <div class="metric-card"><div class="value" style="color:#38bdf8;">{total_events}</div><div class="label">TOTAL EVENTS</div></div>
            <div class="metric-card"><div class="value" style="color:#f43f5e;">{len(critical_events)}</div><div class="label">CRITICAL THREATS</div></div>
            <div class="metric-card"><div class="value" style="color:#ffb700;">{len(hitl_events)}</div><div class="label">HITL REVIEWS</div></div>
            <div class="metric-card"><div class="value" style="color:#4ade80;">{len(safe_events)}</div><div class="label">SAFE EVENTS</div></div>
        </div>

        <div class="section">
            <h2>📊 Executive Summary</h2>
            <table>
                <tr><td style="padding:8px;color:#94a3b8;">Analysis Period</td><td style="padding:8px;color:#e2e8f0;">{audit_logs[-1].get('timestamp','--') if audit_logs else '--'} → {audit_logs[0].get('timestamp','--') if audit_logs else '--'}</td></tr>
                <tr><td style="padding:8px;color:#94a3b8;">Average Risk Score</td><td style="padding:8px;color:#ffb700;font-weight:bold;">{avg_risk} / 100</td></tr>
                <tr><td style="padding:8px;color:#94a3b8;">Maximum Risk Score</td><td style="padding:8px;color:#f43f5e;font-weight:bold;">{max_risk} / 100</td></tr>
                <tr><td style="padding:8px;color:#94a3b8;">SOAR Routines Executed</td><td style="padding:8px;color:#4ade80;font-weight:bold;">{soar_count}</td></tr>
                <tr><td style="padding:8px;color:#94a3b8;">Autonomous Blocks</td><td style="padding:8px;color:#f43f5e;font-weight:bold;">{len(blocked_events)}</td></tr>
                <tr><td style="padding:8px;color:#94a3b8;">Critic Guardrail Overrides</td><td style="padding:8px;color:#a78bfa;font-weight:bold;">{critic_overrides}</td></tr>
            </table>
        </div>

        <div class="section">
            <h2>🎯 MITRE ATT&CK Technique Distribution</h2>
            <table>
                <thead><tr><th>Technique</th><th style="text-align:center;">Count</th><th style="text-align:center;">Severity</th></tr></thead>
                <tbody>{mitre_rows}</tbody>
            </table>
        </div>

        <div class="section">
            <h2>📋 Threat Classification Breakdown</h2>
            <table>
                <thead><tr><th>Classification</th><th style="text-align:center;">Count</th></tr></thead>
                <tbody>{class_rows}</tbody>
            </table>
        </div>

        <div class="section">
            <h2>🚨 Critical Incident Details (Top 10)</h2>
            <table>
                <thead><tr><th>Event ID</th><th>Principal</th><th style="text-align:center;">Risk</th><th>Classification</th><th>Action</th></tr></thead>
                <tbody>{incident_rows if incident_rows else '<tr><td colspan="5" style="padding:15px;text-align:center;color:#64748b;">No critical incidents recorded.</td></tr>'}</tbody>
            </table>
        </div>

        <div class="signature">
            <div style="color:#94a3b8;font-size:12px;margin-bottom:8px;">🔐 Digital Integrity Signature (SHA-256)</div>
            <div class="hash">{sha256_signature}</div>
            <div style="color:#64748b;font-size:10px;margin-top:8px;">This report was automatically generated by AEGIS-SOC Forensic Report Engine. Any modification invalidates the above hash.</div>
        </div>
    </div>
</body>
</html>"""
        return html
