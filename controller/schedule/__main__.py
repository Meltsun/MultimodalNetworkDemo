from pathlib import Path
import sys
root=Path(__file__).parent
sys.path.append(str(root))

from src.ddqn import main
main()