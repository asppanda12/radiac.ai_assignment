import logging
from typing import Dict, Optional
import time

class MetricsLogger:
    def __init__(self):
        """Initialize the metrics logger."""
        self.logger = logging.getLogger("campaign_metrics")
        self.logger.setLevel(logging.INFO)
        
        # Add file handler
        handler = logging.FileHandler("campaign_metrics.log")
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        self.logger.addHandler(handler)
        
        # Initialize metrics
        self.reset_metrics()
    
    def reset_metrics(self):
        """Reset all metrics for a new campaign."""
        self.metrics = {
            "token_counts": {
                "system_prompt": 0,
                "user_prompt": 0,
                "completion": 0
            },
            "processing_time": 0,
            "hallucination_flags": [],
            "validation_errors": [],
            "completion_successful": False
        }
    
    def log_token_count(self, prompt_type: str, count: int):
        """Log token count for different parts of the process."""
        self.metrics["token_counts"][prompt_type] = count
        self.logger.info(f"Token count for {prompt_type}: {count}")
    
    def log_hallucination(self, message: str, confidence: float):
        """Log potential hallucination with confidence score."""
        self.metrics["hallucination_flags"].append({
            "message": message,
            "confidence": confidence
        })
        self.logger.warning(f"Potential hallucination: {message} (confidence: {confidence})")
    
    def log_validation_error(self, error: str):
        """Log validation errors."""
        self.metrics["validation_errors"].append(error)
        self.logger.error(f"Validation error: {error}")
    
    def start_processing(self):
        """Start timing the processing."""
        self.start_time = time.time()
    
    def end_processing(self, success: bool = True):
        """End timing and log success status."""
        self.metrics["processing_time"] = time.time() - self.start_time
        self.metrics["completion_successful"] = success
        self.logger.info(
            f"Processing completed in {self.metrics['processing_time']:.2f}s "
            f"(success: {success})"
        )
    
    def get_metrics(self) -> Dict:
        """Get the current metrics."""
        return self.metrics.copy()
    
    def log_summary(self):
        """Log a summary of all metrics."""
        self.logger.info("Campaign Generation Summary:")
        self.logger.info(f"Total tokens used: {sum(self.metrics['token_counts'].values())}")
        self.logger.info(f"Processing time: {self.metrics['processing_time']:.2f}s")
        self.logger.info(f"Hallucination flags: {len(self.metrics['hallucination_flags'])}")
        self.logger.info(f"Validation errors: {len(self.metrics['validation_errors'])}")
        self.logger.info(f"Success: {self.metrics['completion_successful']}")
