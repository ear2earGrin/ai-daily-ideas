"""Extraction and classification logic for pain points (v1: heuristic/deterministic)."""

import json
import re
import subprocess
from typing import Callable, List, Dict, Optional
from .models import PainPoint


class HeuristicExtractor:
    """
    Extract pain points from text using heuristic rules (v1).
    
    This is a deterministic approach for the prototype.
    In v2, this will be replaced with local Qwen LLM extraction.
    """
    
    # Common pain indicators
    PAIN_PATTERNS = [
        r"(?:i|we) (?:hate|frustrated|tired|annoyed|struggle|spend too much time)",
        r"(?:wish|need|want) (?:there was|a tool|an app|a way)",
        r"manually (?:doing|entering|copying|syncing|updating)",
        r"takes (?:me|us) (?:\d+) hours? (?:every|per)",
        r"no good (?:solution|tool|way) (?:for|to)",
        r"existing tools? (?:are|is) too (?:expensive|complex|clunky)",
    ]
    
    # Audience indicators
    AUDIENCE_PATTERNS = {
        "developers": [r"developer", r"programmer", r"coder", r"engineer", r"dev team"],
        "small business owners": [r"small business", r"shop owner", r"smb", r"sole proprietor"],
        "freelancers": [r"freelancer", r"independent contractor", r"consultant", r"solopreneur"],
        "marketers": [r"marketer", r"marketing team", r"seo", r"content creator"],
        "e-commerce": [r"e-commerce", r"online store", r"shopify", r"woocommerce"],
        "saas founders": [r"saas", r"startup", r"founder", r"bootstrapper"],
    }
    
    def extract(self, text: str, source_url: str = "", source_type: str = "text") -> List[PainPoint]:
        """
        Extract pain points from text using heuristic rules.
        
        Args:
            text: Raw text to analyze
            source_url: URL of the source
            source_type: Type of source (reddit, hn, web, etc.)
        
        Returns:
            List of extracted PainPoint objects
        """
        pain_points = []
        
        # Split into sentences or paragraphs
        segments = self._segment_text(text)
        
        for segment in segments:
            if self._contains_pain_signal(segment):
                pain = self._extract_pain_point(segment, source_url, source_type)
                if pain:
                    pain_points.append(pain)
        
        return pain_points
    
    def _segment_text(self, text: str) -> List[str]:
        """Split text into analyzable segments."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]\s+', text)
        # Filter out very short segments
        return [s.strip() for s in sentences if len(s.strip()) > 50]
    
    def _contains_pain_signal(self, text: str) -> bool:
        """Check if text contains pain indicators."""
        text_lower = text.lower()
        for pattern in self.PAIN_PATTERNS:
            if re.search(pattern, text_lower):
                return True
        return False
    
    def _extract_pain_point(self, text: str, source_url: str, source_type: str) -> Optional[PainPoint]:
        """Extract structured pain point from text segment."""
        text_lower = text.lower()
        
        # Detect audience
        audience = self._detect_audience(text_lower)
        if not audience:
            audience = "general users"
        
        # Extract pain description (simplified heuristic)
        pain_desc = self._extract_pain_description(text_lower)
        
        # Extract workaround if mentioned
        workaround = self._extract_workaround(text_lower)
        
        # Extract existing tools if mentioned
        existing_tools = self._extract_existing_tools(text_lower)
        
        # Create pain point with initial heuristic scores
        pain = PainPoint(
            source_url=source_url,
            source_type=source_type,
            quote=text.strip(),
            audience=audience,
            pain=pain_desc,
            workaround=workaround,
            existing_tools=existing_tools,
            confidence="medium",
            processed_by="heuristic-extractor-v1",
        )
        
        # Apply heuristic scoring
        pain = self._apply_heuristic_scores(pain)
        
        return pain
    
    def _detect_audience(self, text: str) -> str:
        """Detect target audience from text."""
        for audience, patterns in self.AUDIENCE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return audience
        return ""
    
    def _extract_pain_description(self, text: str) -> str:
        """Extract the core pain description."""
        # Look for manual labor patterns
        match = re.search(r"manually (\w+(?:\s+\w+){1,4})", text)
        if match:
            return f"manual {match.group(1)}"
        
        # Look for "takes X hours" patterns
        match = re.search(r"takes.*?(\d+)\s*hours?.*?(every|per)\s+(\w+)", text)
        if match:
            return f"time-consuming process ({match.group(1)}h per {match.group(3)})"
        
        # Look for "no good solution" patterns
        match = re.search(r"no good (?:solution|tool|way) (?:for|to) ([\w\s]{3,30})", text)
        if match:
            return f"lack of solution for {match.group(1).strip()}"
        
        # Default: return truncated text
        return text[:100]
    
    def _extract_workaround(self, text: str) -> str:
        """Extract current workaround if mentioned."""
        match = re.search(r"(?:currently|now|manually) (?:using|doing|via) ([\w\s]{3,50})", text)
        if match:
            return match.group(1).strip()
        
        if "manually" in text:
            return "manual workaround"
        
        return ""
    
    def _extract_existing_tools(self, text: str) -> List[str]:
        """Extract mentions of existing tools."""
        tools = []
        
        # Common tool name patterns
        tool_patterns = [
            r"(zapier|airtable|notion|excel|sheets|slack|trello|asana)",
            r"(\w+\s+(?:tool|app|software|platform|service))",
        ]
        
        for pattern in tool_patterns:
            matches = re.findall(pattern, text)
            tools.extend(matches)
        
        return list(set(tools[:5]))  # Limit to 5 unique tools
    
    def _apply_heuristic_scores(self, pain: PainPoint) -> PainPoint:
        """Apply simple heuristic scoring (0-5 scale)."""
        text_lower = pain.quote.lower()
        
        # Intensity: based on strong language
        strong_words = ["hate", "frustrated", "nightmare", "terrible", "awful"]
        pain.intensity = 4 if any(word in text_lower for word in strong_words) else 3
        
        # Frequency: based on time mentions
        if re.search(r"(?:every|per) (?:day|daily|hour)", text_lower):
            pain.frequency = 5
        elif re.search(r"(?:every|per) (?:week|weekly)", text_lower):
            pain.frequency = 4
        else:
            pain.frequency = 3
        
        # Buyer quality: based on audience
        buyer_scores = {
            "developers": 4,
            "small business owners": 4,
            "saas founders": 5,
            "e-commerce": 4,
            "freelancers": 3,
            "marketers": 3,
        }
        pain.buyer_quality = buyer_scores.get(pain.audience, 3)
        
        # Workaround cost: if manual work is mentioned
        if "manually" in text_lower or pain.workaround:
            pain.workaround_cost = 4
        else:
            pain.workaround_cost = 2
        
        # Existing spend: if cost is mentioned
        if re.search(r"\$\d+", text_lower):
            pain.existing_spend = 3
        else:
            pain.existing_spend = 2
        
        # Reachability: default medium-high for public sources
        pain.reachability = 4
        
        # MVP simplicity: default medium (requires human judgment)
        pain.mvp_simplicity = 3

        # Competition gap: default medium (requires research)
        pain.competition_gap = 3
        
        return pain


def default_command_runner(command: str, prompt: str) -> str:
    """Run an external LLM command with the extraction prompt on stdin."""
    result = subprocess.run(
        command,
        input=prompt,
        text=True,
        shell=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"extractor command failed with exit {result.returncode}")
    return result.stdout


class StructuredExtractor:
    """Extract pain points from text using a structured JSON-producing LLM command."""

    def __init__(self, command: str, runner: Optional[Callable[[str, str], str]] = None):
        if not command:
            raise ValueError("StructuredExtractor requires a command")
        self.command = command
        self.runner = runner or default_command_runner

    def extract(self, text: str, source_url: str = "", source_type: str = "text") -> List[PainPoint]:
        prompt = self._build_prompt(text, source_url, source_type)
        raw = self.runner(self.command, prompt)
        payload = self._parse_json(raw)
        pains = []
        for item in payload.get("pain_points", []):
            pain = self._item_to_pain(item, source_url, source_type)
            if pain is not None:
                pains.append(pain)
        return pains

    def _build_prompt(self, text: str, source_url: str, source_type: str) -> str:
        return f"""You extract monetizable B2B/SaaS pain points from public posts.
Return strict JSON only, no markdown, no prose.
Schema:
{{
  "pain_points": [
    {{
      "quote": "verbatim sentence or compact excerpt from source",
      "pain": "specific painful workflow",
      "audience": "who has the pain",
      "workaround": "current workaround if present, else empty string",
      "existing_tools": ["tools mentioned"],
      "confidence": "high|medium|low"
    }}
  ]
}}
Rules:
- Only extract concrete workflow pains, not vague opinions.
- Prefer business, productivity, compliance, devtool, finance, ops, or admin pains.
- Quote must be grounded in the source text.
- If no concrete pain exists, return {{"pain_points": []}}.

Source URL: {source_url}
Source type: {source_type}
Source text:
{text[:12000]}
"""

    def _parse_json(self, raw: str) -> Dict:
        raw = raw.strip()
        if raw.startswith("```"):
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("structured extractor output must be a JSON object")
        if not isinstance(data.get("pain_points", []), list):
            raise ValueError("pain_points must be a list")
        return data

    def _item_to_pain(self, item: Dict, source_url: str, source_type: str) -> Optional[PainPoint]:
        quote = str(item.get("quote") or "").strip()
        pain_desc = str(item.get("pain") or "").strip()
        audience = str(item.get("audience") or "").strip() or "general users"
        if len(quote) < 25 or len(pain_desc) < 3:
            return None
        existing_tools = item.get("existing_tools") or []
        if not isinstance(existing_tools, list):
            existing_tools = []
        pain = PainPoint(
            source_url=source_url,
            source_type=source_type,
            quote=quote,
            audience=audience,
            pain=pain_desc,
            workaround=str(item.get("workaround") or "").strip(),
            existing_tools=[str(tool) for tool in existing_tools[:5]],
            confidence=str(item.get("confidence") or "medium").strip() or "medium",
            processed_by="structured-extractor-v1",
        )
        HeuristicExtractor()._apply_heuristic_scores(pain)
        pain.total_score = sum([
            pain.intensity,
            pain.frequency,
            pain.buyer_quality,
            pain.workaround_cost,
            pain.existing_spend,
            pain.reachability,
            pain.mvp_simplicity,
            pain.competition_gap,
        ])
        return pain
