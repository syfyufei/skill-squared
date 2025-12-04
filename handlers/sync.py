"""
Sync operations for skill-squared
Handles synchronization between standalone skills and marketplaces
"""

import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class SyncResult:
    """Container for sync operation results"""

    def __init__(self):
        self.copied_files = []
        self.skipped_files = []
        self.errors = []
        self.backups = []

    def add_copied(self, file_path: str):
        """Record a copied file"""
        self.copied_files.append(file_path)

    def add_skipped(self, file_path: str, reason: str):
        """Record a skipped file"""
        self.skipped_files.append({'file': file_path, 'reason': reason})

    def add_error(self, message: str):
        """Record an error"""
        self.errors.append(message)

    def add_backup(self, file_path: str, backup_path: str):
        """Record a backup"""
        self.backups.append({'original': file_path, 'backup': backup_path})

    def is_success(self) -> bool:
        """Check if sync succeeded"""
        return len(self.errors) == 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'success': self.is_success(),
            'copied_files': self.copied_files,
            'skipped_files': self.skipped_files,
            'backups': self.backups,
            'errors': self.errors
        }


class SkillSync:
    """Manages skill synchronization operations"""

    def __init__(self, config_path: str = None):
        """
        Initialize skill sync

        Args:
            config_path: Path to config.json (optional)
        """
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load sync configuration"""
        if config_path:
            config_file = Path(config_path)
        else:
            # Default to config/config.json in project root
            project_root = Path(__file__).parent.parent
            config_file = project_root / 'config' / 'config.json'

        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Return default config
            return {
                'sync': {
                    'backup_enabled': True,
                    'backup_suffix': '.backup',
                    'confirm_overwrite': True,
                    'files_to_sync': [
                        'skills/{skill_name}.md',
                        '.claude/commands/'
                    ]
                }
            }

    def sync(self, source_dir: str, target_dir: str, skill_name: str, dry_run: bool = False) -> SyncResult:
        """
        Sync skill files from source to target

        Args:
            source_dir: Source skill directory (standalone repo)
            target_dir: Target directory (marketplace)
            skill_name: Name of the skill
            dry_run: If True, only show what would be synced without actually copying

        Returns:
            SyncResult object
        """
        result = SyncResult()
        source_path = Path(source_dir)
        target_path = Path(target_dir)

        # Validate paths
        if not source_path.exists():
            result.add_error(f"Source directory not found: {source_dir}")
            return result

        if not target_path.exists():
            result.add_error(f"Target directory not found: {target_dir}")
            return result

        # Get files to sync from config
        sync_patterns = self.config['sync']['files_to_sync']

        for pattern in sync_patterns:
            # Substitute skill_name
            file_pattern = pattern.replace('{skill_name}', skill_name)

            if file_pattern.endswith('/'):
                # Directory sync
                self._sync_directory(
                    source_path / file_pattern.rstrip('/'),
                    target_path / file_pattern.rstrip('/'),
                    result,
                    dry_run
                )
            else:
                # File sync
                self._sync_file(
                    source_path / file_pattern,
                    target_path / file_pattern,
                    result,
                    dry_run
                )

        return result

    def _sync_file(self, source_file: Path, target_file: Path, result: SyncResult, dry_run: bool):
        """Sync a single file"""
        if not source_file.exists():
            result.add_skipped(str(source_file), "Source file not found")
            return

        # Create target directory if needed
        target_file.parent.mkdir(parents=True, exist_ok=True)

        # Backup existing file if enabled
        if target_file.exists() and self.config['sync']['backup_enabled']:
            backup_path = self._create_backup(target_file, dry_run)
            if backup_path:
                result.add_backup(str(target_file), str(backup_path))

        # Copy file
        if not dry_run:
            try:
                shutil.copy2(source_file, target_file)
                result.add_copied(str(target_file.relative_to(target_file.parents[len(source_file.parents) - 1])))
            except Exception as e:
                result.add_error(f"Failed to copy {source_file}: {str(e)}")
        else:
            result.add_copied(f"[DRY RUN] {target_file}")

    def _sync_directory(self, source_dir: Path, target_dir: Path, result: SyncResult, dry_run: bool):
        """Sync all files in a directory"""
        if not source_dir.exists():
            result.add_skipped(str(source_dir), "Source directory not found")
            return

        # Get all files in source directory
        for source_file in source_dir.rglob('*'):
            if source_file.is_file():
                # Calculate relative path
                rel_path = source_file.relative_to(source_dir)
                target_file = target_dir / rel_path

                self._sync_file(source_file, target_file, result, dry_run)

    def _create_backup(self, file_path: Path, dry_run: bool) -> Optional[Path]:
        """
        Create backup of existing file

        Args:
            file_path: File to backup
            dry_run: If True, don't actually create backup

        Returns:
            Path to backup file or None if backup failed
        """
        if not file_path.exists():
            return None

        # Generate backup path with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_suffix = self.config['sync']['backup_suffix']
        backup_path = file_path.with_suffix(f'{backup_suffix}.{timestamp}{file_path.suffix}')

        if not dry_run:
            try:
                shutil.copy2(file_path, backup_path)
                return backup_path
            except Exception:
                return None
        else:
            return backup_path

    def list_sync_files(self, source_dir: str, skill_name: str) -> List[str]:
        """
        List files that would be synced

        Args:
            source_dir: Source skill directory
            skill_name: Name of the skill

        Returns:
            List of file paths
        """
        source_path = Path(source_dir)
        files = []

        sync_patterns = self.config['sync']['files_to_sync']

        for pattern in sync_patterns:
            file_pattern = pattern.replace('{skill_name}', skill_name)

            if file_pattern.endswith('/'):
                # Directory
                dir_path = source_path / file_pattern.rstrip('/')
                if dir_path.exists():
                    files.extend([
                        str(f.relative_to(source_path))
                        for f in dir_path.rglob('*')
                        if f.is_file()
                    ])
            else:
                # File
                file_path = source_path / file_pattern
                if file_path.exists():
                    files.append(str(file_path.relative_to(source_path)))

        return files


def sync_skill(source_dir: str, target_dir: str, skill_name: str, dry_run: bool = False, config_path: str = None) -> Dict[str, Any]:
    """
    Convenience function for skill sync

    Args:
        source_dir: Source skill directory
        target_dir: Target marketplace directory
        skill_name: Name of the skill
        dry_run: If True, only show what would be synced
        config_path: Optional config path

    Returns:
        Sync result dictionary
    """
    syncer = SkillSync(config_path)
    result = syncer.sync(source_dir, target_dir, skill_name, dry_run)
    return result.to_dict()
