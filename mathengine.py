from dataclasses import dataclass
from typing import List, Dict, Optional
from decimal import Decimal
import json
from enum import Enum
import random


class GameMathType(Enum):
    LINES = "LINES"


class MathModelType(Enum):
    FINITE = "FINITE"
    TRUE_RANDOM = "TRUE_RANDOM"


@dataclass
class MathSetting:
    name: str
    version: int
    model_type: MathModelType
    cycle_size: Optional[int] = None  # For FINITE model
    cycle_position: Optional[int] = None  # For FINITE model

    @classmethod
    def from_dict(cls, data: dict) -> 'MathSetting':
        model_type = MathModelType(data.get('model_type', 'TRUE_RANDOM'))
        return cls(
            name=GameMathType(data['name']),
            version=data['version'],
            model_type=model_type,
            cycle_size=data.get('cycle_size'),
            cycle_position=data.get('cycle_position', 0) if model_type == MathModelType.FINITE else None
        )


@dataclass
class RTPConfig:
    id: str
    min_ret: Decimal
    max_ret: Decimal
    weight: int = 1  # For FINITE model distribution

    @classmethod
    def from_dict(cls, data: dict) -> 'RTPConfig':
        return cls(
            id=data['id'],
            min_ret=Decimal(data['min_ret']),
            max_ret=Decimal(data['max_ret']),
            weight=data.get('weight', 1)
        )


@dataclass
class BetConfig:
    id: str
    lines: int
    bpl: int  # bet per line
    denom: int

    @classmethod
    def from_dict(cls, data: dict) -> 'BetConfig':
        return cls(
            id=data['id'],
            lines=data['lines'],
            bpl=data['bpl'],
            denom=data['denom']
        )


@dataclass
class SpinResult:
    """Represents the result of a single spin"""
    total_bet: int
    win_amount: int
    rtp_config: RTPConfig
    actual_return_percentage: float


class GameMathEngine:
    def __init__(self, config_file: str):
        self.config = self._load_config(config_file)
        self.game_code = self.config['game_code']
        self.game_name = self.config['game_name']
        self.math_setting = MathSetting.from_dict(self.config['math_setting']['type'])
        self.line_settings = self._parse_line_settings()
        self.denomination_settings = self._parse_denomination_settings()
        self.bet_multiplier_settings = self._parse_bet_multiplier_settings()
        self.rtp_configs = self._parse_rtp_configs()
        self.bet_configs = self._parse_bet_configs()
        
        # Initialize finite model state if needed
        if self.math_setting.model_type == MathModelType.FINITE:
            self._initialize_finite_model()

    def _initialize_finite_model(self):
        """Initialize the finite model with cycle data"""
        if not self.math_setting.cycle_size:
            raise ValueError("Cycle size must be specified for FINITE math model")
        
        # Create weighted RTP distribution for the cycle
        self.cycle_rtps = []
        for rtp in self.rtp_configs:
            self.cycle_rtps.extend([rtp] * rtp.weight)
        
        # Ensure cycle size matches total weights
        if len(self.cycle_rtps) != self.math_setting.cycle_size:
            raise ValueError(f"Total RTP weights ({len(self.cycle_rtps)}) must match cycle size ({self.math_setting.cycle_size})")
        
        # Shuffle the cycle
        random.shuffle(self.cycle_rtps)

    def _load_config(self, config_file: str) -> dict:
        """Load configuration from JSON file or string."""
        if isinstance(config_file, str):
            try:
                return json.loads(config_file)
            except json.JSONDecodeError:
                with open(config_file, 'r') as f:
                    return json.load(f)
        return config_file

    def _parse_line_settings(self) -> List[int]:
        """Parse line settings from configuration."""
        settings = self.config['line_settings']
        if settings['type'] == 'list_from_math_config':
            return sorted(settings['values'])
        raise ValueError(f"Unsupported line settings type: {settings['type']}")

    def _parse_denomination_settings(self) -> List[int]:
        """Parse denomination settings from configuration."""
        settings = self.config['denomination_settings']
        if settings['type'] == 'range_by_math_config':
            return sorted(settings['values'])
        raise ValueError(f"Unsupported denomination settings type: {settings['type']}")

    def _parse_bet_multiplier_settings(self) -> Dict:
        """Parse bet multiplier settings from configuration."""
        settings = self.config['bet_multiplier_per_denomination_settings']
        return {
            'min_count': settings['bet_button_min_count'],
            'max_count': settings['bet_button_max_count'],
            'values': sorted(settings['bet_button_values'])
        }

    def _parse_rtp_configs(self) -> List[RTPConfig]:
        """Parse RTP configurations."""
        return [RTPConfig.from_dict(rtp) for rtp in self.config['rtp']]

    def _parse_bet_configs(self) -> List[BetConfig]:
        """Parse bet configurations."""
        return [BetConfig.from_dict(bet) for bet in self.config['bets']]

    def calculate_total_bet(self, lines: int, bet_per_line: int, denomination: int) -> int:
        """Calculate total bet amount."""
        if lines not in self.line_settings:
            raise ValueError(f"Invalid number of lines: {lines}")
        if denomination not in self.denomination_settings:
            raise ValueError(f"Invalid denomination: {denomination}")
        if bet_per_line not in self.bet_multiplier_settings['values']:
            raise ValueError(f"Invalid bet per line: {bet_per_line}")
        
        return lines * bet_per_line * denomination

    def _get_next_rtp(self) -> RTPConfig:
        """Get next RTP based on math model type."""
        if self.math_setting.model_type == MathModelType.FINITE:
            # Get RTP from cycle and update position
            rtp = self.cycle_rtps[self.math_setting.cycle_position]
            self.math_setting.cycle_position = (self.math_setting.cycle_position + 1) % self.math_setting.cycle_size
            return rtp
        else:
            # True random selection based on weights
            total_weight = sum(rtp.weight for rtp in self.rtp_configs)
            r = random.randint(1, total_weight)
            current_weight = 0
            for rtp in self.rtp_configs:
                current_weight += rtp.weight
                if r <= current_weight:
                    return rtp
            return self.rtp_configs[-1]  # Fallback to last RTP

    def spin(self, lines: int, bet_per_line: int, denomination: int) -> SpinResult:
        """
        Execute a single spin and return the structured result
        """
        total_bet = self.calculate_total_bet(lines, bet_per_line, denomination)
        selected_rtp = self._get_next_rtp()
        
        # Calculate win with some volatility
        rtp_value = float(selected_rtp.min_ret) / 100
        actual_return = rtp_value * random.uniform(0.8, 1.2)
        win_amount = int(total_bet * actual_return)
        
        return SpinResult(
            total_bet=total_bet,
            win_amount=win_amount,
            rtp_config=selected_rtp,
            actual_return_percentage=actual_return * 100
        )

    def get_available_bets(self, denomination: Optional[int] = None) -> List[BetConfig]:
        """Get available bet configurations, optionally filtered by denomination."""
        if denomination is None:
            return self.bet_configs
        return [bet for bet in self.bet_configs if bet.denom == denomination]

    def get_rtp_by_id(self, rtp_id: str) -> Optional[RTPConfig]:
        """Get RTP configuration by ID."""
        for rtp in self.rtp_configs:
            if rtp.id == rtp_id:
                return rtp
        return None

    def validate_bet(self, lines: int, bet_per_line: int, denomination: int) -> bool:
        """Validate if a bet configuration is valid."""
        try:
            self.calculate_total_bet(lines, bet_per_line, denomination)
            return True
        except ValueError:
            return False

    def get_bet_range(self, denomination: int) -> Dict[str, int]:
        """Get minimum and maximum bet for a given denomination."""
        valid_bets = self.get_available_bets(denomination)
        if not valid_bets:
            raise ValueError(f"No valid bets for denomination: {denomination}")
        
        total_bets = [self.calculate_total_bet(bet.lines, bet.bpl, bet.denom) 
                     for bet in valid_bets]
        return {
            'min_bet': min(total_bets),
            'max_bet': max(total_bets)
        }

    def get_available_lines(self, denomination: int) -> List[int]:
        """Get available lines for a given denomination."""
        valid_bets = self.get_available_bets(denomination)
        return sorted(list(set(bet.lines for bet in valid_bets)))
