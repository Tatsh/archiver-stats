local utils = import 'utils.libjsonnet';

{
  uses_user_defaults: true,
  description: 'Reusable live statistics and progress display for CLIs.',
  keywords: ['cli', 'progress', 'rich', 'statistics', 'status'],
  project_name: 'archiver-stats',
  version: '0.0.1',
  python_deps+: {
    main+: {
      rich: utils.latestPypiPackageVersionCaret('rich'),
    },
  },
}
