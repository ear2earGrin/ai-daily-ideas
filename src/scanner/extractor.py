"""Extraction and classification logic for pain points (v1: heuristic/deterministic)."""

import re
from typing import List, Dict, Optional
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
