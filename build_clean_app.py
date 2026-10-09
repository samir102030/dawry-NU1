import re

# Read current INITIAL_TEAMS from src/App.tsx
with open('src/App.tsx', 'r', encoding='utf-8') as f:
    orig = f.read()

teams_match = re.search(r'const INITIAL_TEAMS: Team\[\] = \[([\s\S]*?)\];', orig)
assert teams_match, "INITIAL_TEAMS not found"
teams_content = teams_match.group(1).strip()

r32_match = re.search(r'export const R32_SEED_PAIRS: Record<string, \{[\s\S]*?\n\};', orig)
assert r32_match, "R32_SEED_PAIRS not found"
r32_content = r32_match.group(0).strip()

code = f'''import React, {{ useState, useMemo }} from 'react';
import confetti from 'canvas-confetti';
import {{ 
  Trophy, 
  Calendar, 
  Shield, 
  CheckCircle2, 
  Search, 
  SlidersHorizontal, 
  Swords, 
  Edit3, 
  Plus, 
  Clock, 
  MapPin, 
  Check, 
  Sparkles,
  Award, 
  Filter, 
  Layers, 
  Target, 
  ChevronRight,
  Eye, 
  RotateCcw, 
  X,
  CalendarDays,
  AlertCircle
}} from 'lucide-react';

// --- TYPES ---
export interface Team {{
  id: string;
  name: string;
  group: string;
  played: number;
  won: number;
  drawn: number;
  lost: number;
  gf: number;
  ga: number;
  gd: number;
  points: number;
  logoColor: string;
}}

export interface Match {{
  id: string;
  group?: string;
  round?: number; // 1 to 5 for group matches
  stage: 'group' | 'r32' | 'r16' | 'qf' | 'sf' | 'final';
  stageName: string;
  teamA: string;
  teamB: string;
  scoreA: number | null;
  scoreB: number | null;
  status: 'upcoming' | 'live' | 'finished';
  minute?: number;
  date: string; // Empty string if not scheduled yet
  time: string; // Empty string if not scheduled yet
  pitch: string; // Empty string if not scheduled yet
  isScheduled: boolean; // True only when the admin has explicitly scheduled it!
  scorersSummary?: string; // Optional notes/scorers
  recordedBy?: string;
}}

export interface Scorekeeper {{
  id: string;
  name: string;
  studentId: string;
  role: 'scorekeeper' | 'admin';
  assignedGroups: string[];
  active: boolean;
}}

// Initial 48 Teams across 8 groups (A to H) - 6 teams in each group
const INITIAL_TEAMS: Team[] = [
{teams_content}
];

// Helper to build all 120 group stage matches (15 matches across 5 rounds for each of the 8 groups)
// Every team plays exactly 5 matches within its group
// ALL MATCHES START UNSCHEDULED (غير محددة الموعد) until the user sets their date/time!
const generateGroupStageMatches = (): Match[] => {{
  const groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];

  // Circle algorithm round-robin pairings for 6 teams (indices 0..5):
  const roundPairings = [
    // Round 1
    [[0, 5], [1, 4], [2, 3]],
    // Round 2
    [[0, 4], [5, 3], [1, 2]],
    // Round 3
    [[0, 3], [4, 2], [5, 1]],
    // Round 4
    [[0, 2], [3, 1], [4, 5]],
    // Round 5
    [[0, 1], [2, 5], [3, 4]],
  ];

  const matchesList: Match[] = [];

  groups.forEach((grp) => {{
    const teamsInGroup = INITIAL_TEAMS.filter(t => t.group === grp);

    roundPairings.forEach((roundPairs, rIdx) => {{
      const roundNum = rIdx + 1;

      roundPairs.forEach((pair, mIdx) => {{
        const teamA = teamsInGroup[pair[0]]?.name || `فريق ${{pair[0] + 1}} (${{grp}})`;
        const teamB = teamsInGroup[pair[1]]?.name || `فريق ${{pair[1] + 1}} (${{grp}})`;
        const id = `grp_${{grp.toLowerCase()}}_r${{roundNum}}_m${{mIdx + 1}}`;

        const matchObj: Match = {{
          id,
          group: grp,
          round: roundNum,
          stage: 'group',
          stageName: `المجموعة ${{grp}} (الجولة ${{roundNum}})`,
          teamA,
          teamB,
          scoreA: null,
          scoreB: null,
          status: 'upcoming',
          date: '', // لا يتم تنزيل الماتش حتى يحدد المستخدم معاده
          time: '',
          pitch: '',
          isScheduled: false, // بانتظار تحديد الموعد من الإدارة
        }};

        matchesList.push(matchObj);
      }});
    }});
  }});

  return matchesList;
}};

// Initial Knockout Bracket Matches (32 matches from Round of 32 down to Grand Final)
// All start unscheduled until reached / scheduled by admin
const INITIAL_KNOCKOUT_MATCHES: Match[] = [
  {{ id: 'r32_1', stage: 'r32', stageName: 'دور الـ 32 (مباراة 1)', teamA: 'أول المجموعة A', teamB: 'رابع المجموعة B', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_2', stage: 'r32', stageName: 'دور الـ 32 (مباراة 2)', teamA: 'ثاني المجموعة A', teamB: 'ثالث المجموعة B', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_3', stage: 'r32', stageName: 'دور الـ 32 (مباراة 3)', teamA: 'ثالث المجموعة A', teamB: 'ثاني المجموعة B', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_4', stage: 'r32', stageName: 'دور الـ 32 (مباراة 4)', teamA: 'رابع المجموعة A', teamB: 'أول المجموعة B', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  
  {{ id: 'r32_5', stage: 'r32', stageName: 'دور الـ 32 (مباراة 5)', teamA: 'أول المجموعة C', teamB: 'رابع المجموعة D', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_6', stage: 'r32', stageName: 'دور الـ 32 (مباراة 6)', teamA: 'ثاني المجموعة C', teamB: 'ثالث المجموعة D', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_7', stage: 'r32', stageName: 'دور الـ 32 (مباراة 7)', teamA: 'ثالث المجموعة C', teamB: 'ثاني المجموعة D', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_8', stage: 'r32', stageName: 'دور الـ 32 (مباراة 8)', teamA: 'رابع المجموعة C', teamB: 'أول المجموعة D', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},

  {{ id: 'r32_9', stage: 'r32', stageName: 'دور الـ 32 (مباراة 9)', teamA: 'أول المجموعة E', teamB: 'رابع المجموعة F', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_10', stage: 'r32', stageName: 'دور الـ 32 (مباراة 10)', teamA: 'ثاني المجموعة E', teamB: 'ثالث المجموعة F', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_11', stage: 'r32', stageName: 'دور الـ 32 (مباراة 11)', teamA: 'ثالث المجموعة E', teamB: 'ثاني المجموعة F', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_12', stage: 'r32', stageName: 'دور الـ 32 (مباراة 12)', teamA: 'رابع المجموعة E', teamB: 'أول المجموعة F', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},

  {{ id: 'r32_13', stage: 'r32', stageName: 'دور الـ 32 (مباراة 13)', teamA: 'أول المجموعة G', teamB: 'رابع المجموعة H', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_14', stage: 'r32', stageName: 'دور الـ 32 (مباراة 14)', teamA: 'ثاني المجموعة G', teamB: 'ثالث المجموعة H', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_15', stage: 'r32', stageName: 'دور الـ 32 (مباراة 15)', teamA: 'ثالث المجموعة G', teamB: 'ثاني المجموعة H', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r32_16', stage: 'r32', stageName: 'دور الـ 32 (مباراة 16)', teamA: 'رابع المجموعة G', teamB: 'أول المجموعة H', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},

  // --- دور الـ 16 (8 مباريات) ---
  {{ id: 'r16_1', stage: 'r16', stageName: 'دور الـ 16 (مباراة 1)', teamA: 'الفائز من م1 (دور 32)', teamB: 'الفائز من م2 (دور 32)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r16_2', stage: 'r16', stageName: 'دور الـ 16 (مباراة 2)', teamA: 'الفائز من م3 (دور 32)', teamB: 'الفائز من م4 (دور 32)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r16_3', stage: 'r16', stageName: 'دور الـ 16 (مباراة 3)', teamA: 'الفائز من م5 (دور 32)', teamB: 'الفائز من م6 (دور 32)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r16_4', stage: 'r16', stageName: 'دور الـ 16 (مباراة 4)', teamA: 'الفائز من م7 (دور 32)', teamB: 'الفائز من م8 (دور 32)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r16_5', stage: 'r16', stageName: 'دور الـ 16 (مباراة 5)', teamA: 'الفائز من م9 (دور 32)', teamB: 'الفائز من م10 (دور 32)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r16_6', stage: 'r16', stageName: 'دور الـ 16 (مباراة 6)', teamA: 'الفائز من م11 (دور 32)', teamB: 'الفائز من م12 (دور 32)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r16_7', stage: 'r16', stageName: 'دور الـ 16 (مباراة 7)', teamA: 'الفائز من م13 (دور 32)', teamB: 'الفائز من م14 (دور 32)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'r16_8', stage: 'r16', stageName: 'دور الـ 16 (مباراة 8)', teamA: 'الفائز من م15 (دور 32)', teamB: 'الفائز من م16 (دور 32)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},

  // --- ربع النهائي (4 مباريات) ---
  {{ id: 'qf1', stage: 'qf', stageName: 'ربع النهائي (1)', teamA: 'المتأهل من دور 16 (1)', teamB: 'المتأهل من دور 16 (2)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'qf2', stage: 'qf', stageName: 'ربع النهائي (2)', teamA: 'المتأهل من دور 16 (3)', teamB: 'المتأهل من دور 16 (4)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'qf3', stage: 'qf', stageName: 'ربع النهائي (3)', teamA: 'المتأهل من دور 16 (5)', teamB: 'المتأهل من دور 16 (6)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'qf4', stage: 'qf', stageName: 'ربع النهائي (4)', teamA: 'المتأهل من دور 16 (7)', teamB: 'المتأهل من دور 16 (8)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},

  // --- نصف النهائي (مباراتان) ---
  {{ id: 'sf1', stage: 'sf', stageName: 'نصف النهائي (1)', teamA: 'المتأهل من ربع النهائي (1)', teamB: 'المتأهل من ربع النهائي (2)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
  {{ id: 'sf2', stage: 'sf', stageName: 'نصف النهائي (2)', teamA: 'المتأهل من ربع النهائي (3)', teamB: 'المتأهل من ربع النهائي (4)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},

  // --- مباراة المركز الثالث والرابع ---
  {{ id: 'third', stage: 'final', stageName: 'مباراة المركز الثالث 🥉', teamA: 'الخاسر من نصف النهائي (1)', teamB: 'الخاسر من نصف النهائي (2)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},

  // --- النهائي الكبير 🏆 ---
  {{ id: 'fin', stage: 'final', stageName: 'النهائي الكبير 🏆', teamA: 'المتأهل للنهائي (1)', teamB: 'المتأهل للنهائي (2)', scoreA: null, scoreB: null, status: 'upcoming', date: '', time: '', pitch: '', isScheduled: false }},
];

// All tournament matches: 120 group stage matches (5 rounds for each group) + 32 knockout matches = 152 matches
const INITIAL_MATCHES: Match[] = [...generateGroupStageMatches(), ...INITIAL_KNOCKOUT_MATCHES];

{r32_content}

const INITIAL_SCOREKEEPERS: Scorekeeper[] = [
  {{ id: 'sk1', name: 'سمير (المدير العام)', studentId: '20210001', role: 'admin', assignedGroups: ['ALL'], active: true }},
  {{ id: 'sk2', name: 'عمر النجار (حكم ومسؤول ملاعب)', studentId: '20220911', role: 'scorekeeper', assignedGroups: ['A', 'B', 'C', 'D'], active: true }},
  {{ id: 'sk3', name: 'كريم وائل (مسجل نتائج)', studentId: '20230112', role: 'scorekeeper', assignedGroups: ['E', 'F', 'G', 'H'], active: true }},
];

export default function App() {{
  const [currentTab, setCurrentTab] = useState<'matches_control' | 'groups' | 'bracket' | 'manage'>('matches_control');
  
  // Data States
  const [teams, setTeams] = useState<Team[]>(INITIAL_TEAMS);
  const [matches, setMatches] = useState<Match[]>(INITIAL_MATCHES);
  const [scorekeepers, setScorekeepers] = useState<Scorekeeper[]>(INITIAL_SCOREKEEPERS);

  // Active Operator
  const [activeOperatorId, setActiveOperatorId] = useState<string>('sk1');

  // Filter States
  const [matchScheduleTab, setMatchScheduleTab] = useState<'scheduled' | 'unscheduled' | 'all'>('scheduled');
  const [matchFilterStatus, setMatchFilterStatus] = useState<'all' | 'upcoming' | 'live' | 'finished'>('all');
  const [matchStageFilter, setMatchStageFilter] = useState<'all' | 'group' | 'r32' | 'r16' | 'finals'>('all');
  const [groupStageRoundFilter, setGroupStageRoundFilter] = useState<'all' | number>('all');
  const [groupStageLetterFilter, setGroupStageLetterFilter] = useState<'all' | string>('all');
  const [manageTeamsGroupFilter, setManageTeamsGroupFilter] = useState<'all' | string>('all');
  const [selectedGroup, setSelectedGroup] = useState<string>('A');
  const [groupsViewMode, setGroupsViewMode] = useState<'table' | 'fixtures' | 'qualified_32'>('table');
  const [bracketStageFilter, setBracketStageFilter] = useState<'all' | 'r32' | 'r16' | 'qf' | 'sf' | 'final'>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Selected Team for viewing all 5 matches
  const [selectedTeamNameForMatches, setSelectedTeamNameForMatches] = useState<string | null>(null);
  const [teamMatchesModalFilter, setTeamMatchesModalFilter] = useState<'all' | 'scheduled' | 'finished'>('all');

  // Bulk Edit / Import Teams States
  const [isBulkEditingTeams, setIsBulkEditingTeams] = useState<boolean>(false);
  const [bulkEditTab, setBulkEditTab] = useState<'by_group' | 'paste_text'>('by_group');
  const [bulkTeamsByGroup, setBulkTeamsByGroup] = useState<Record<string, string[]>>({{}});
  const [bulkTeamsText, setBulkTeamsText] = useState<string>('');

  // Modals
  const [schedulingMatch, setSchedulingMatch] = useState<Match | null>(null);
  const [recordingResultMatch, setRecordingResultMatch] = useState<Match | null>(null);
  const [editingTeam, setEditingTeam] = useState<Team | null>(null);
  const [isAddingMatch, setIsAddingMatch] = useState<boolean>(false);

  // Form states for Match Schedule / Reschedule
  const [scheduleForm, setScheduleForm] = useState({{
    date: '',
    time: '04:00 م',
    pitch: 'الملعب الرئيسي (A)',
  }});

  // Result Recording Form
  const [resultForm, setResultForm] = useState({{
    scoreA: 0,
    scoreB: 0,
    status: 'finished' as 'live' | 'finished',
    minute: 90,
    notes: '',
  }});

  // Add Custom Match Form
  const [newMatchForm, setNewMatchForm] = useState({{
    stageName: 'مباراة دور المجموعات',
    stage: 'group' as 'group' | 'r32' | 'r16' | 'qf' | 'sf' | 'final',
    teamA: INITIAL_TEAMS[0].name,
    teamB: INITIAL_TEAMS[1].name,
    date: '',
    time: '04:00 م',
    pitch: 'الملعب الرئيسي (A)',
  }});

  // Manage Sub-tab: teams | scorekeepers
  const [manageSubTab, setManageSubTab] = useState<'teams' | 'scorekeepers'>('teams');

  // New Scorekeeper Form
  const [newScorekeeperForm, setNewScorekeeperForm] = useState({{
    name: '',
    studentId: '',
    assignedGroups: 'ALL',
  }});

  const currentOperator = useMemo(() => {{
    return scorekeepers.find(sk => sk.id === activeOperatorId) || scorekeepers[0];
  }}, [scorekeepers, activeOperatorId]);

  // --- تصفير جميع المباريات والنتائج والفرق ---
  const handleResetAllMatches = () => {{
    if (confirm('هل أنت متأكد من تصفير جميع المباريات والنتائج؟\\nسيتم إعادة جميع الـ 120 مباراة في دور المجموعات ومباريات البطولة إلى حالة (قادمة)، وتصفير أهداف ونقاط كافة الفرق.')) {{
      setMatches(prev => prev.map(m => ({{
        ...m,
        scoreA: null,
        scoreB: null,
        status: 'upcoming' as const,
        minute: undefined,
        scorersSummary: undefined,
        recordedBy: undefined,
      }})));
      setTeams(prev => prev.map(t => ({{
        ...t,
        played: 0,
        won: 0,
        drawn: 0,
        lost: 0,
        gf: 0,
        ga: 0,
        gd: 0,
        points: 0,
      }})));
      confetti({{ particleCount: 50, spread: 60 }});
      alert('تم تصفير جميع الماتشات والنتائج بنجاح! جميع الفرق تبدأ الآن بـ 0 نقاط و0 أهداف.');
    }}
  }};

  // --- SCHEDULING HANDLERS ---
  const handleOpenScheduleModal = (match: Match) => {{
    setSchedulingMatch(match);
    setScheduleForm({{
      date: match.date || '',
      time: match.time || '04:00 م',
      pitch: match.pitch || 'الملعب الرئيسي (A)',
    }});
  }};

  const handleSaveSchedule = (e: React.FormEvent) => {{
    e.preventDefault();
    if (!schedulingMatch) return;
    if (!scheduleForm.date) {{
      alert('يرجى اختيار تاريخ ويوم إقامة المباراة أولاً!');
      return;
    }}

    setMatches(prev => prev.map(m => {{
      if (m.id === schedulingMatch.id) {{
        return {{
          ...m,
          date: scheduleForm.date,
          time: scheduleForm.time || '04:00 م',
          pitch: scheduleForm.pitch || 'الملعب الرئيسي (A)',
          isScheduled: true, // الآن أصبحت المباراة منزّلة رسمياً في الجدول
          recordedBy: `${{currentOperator.name}} (تحديد موعد)`,
        }};
      }}
      return m;
    }}));

    setSchedulingMatch(null);
    confetti({{ particleCount: 50, spread: 60, origin: {{ y: 0.6 }} }});
    alert(`تم تحديد ميعاد المباراة (${{schedulingMatch.teamA}} ضد ${{schedulingMatch.teamB}}) وتنزيلها في جدول البطولة بنجاح! 📅`);
  }};

  const handleUnscheduleMatch = (matchId: string) => {{
    if (confirm('هل ترغب في سحب هذه المباراة من الجدول وإلغاء موعدها لتعود لحالة بانتظار تحديد الموعد؟')) {{
      setMatches(prev => prev.map(m => {{
        if (m.id === matchId) {{
          return {{
            ...m,
            date: '',
            time: '',
            pitch: '',
            isScheduled: false,
          }};
        }}
        return m;
      }}));
      setSchedulingMatch(null);
      alert('تم سحب المباراة بنجاح وعادت لقائمة بانتظار تحديد الموعد.');
    }}
  }};

  // --- RESULT RECORDING HANDLERS ---
  const handleOpenResultModal = (match: Match) => {{
    setRecordingResultMatch(match);
    setResultForm({{
      scoreA: match.scoreA !== null ? match.scoreA : 0,
      scoreB: match.scoreB !== null ? match.scoreB : 0,
      status: match.status === 'live' ? 'live' : 'finished',
      minute: match.minute || 90,
      notes: match.scorersSummary || '',
    }});
  }};

  const handleSaveMatchResult = (e: React.FormEvent) => {{
    e.preventDefault();
    if (!recordingResultMatch) return;

    const sA = Number(resultForm.scoreA);
    const sB = Number(resultForm.scoreB);

    setMatches(prev => prev.map(m => {{
      if (m.id === recordingResultMatch.id) {{
        return {{
          ...m,
          scoreA: sA,
          scoreB: sB,
          status: resultForm.status,
          minute: resultForm.status === 'live' ? Number(resultForm.minute) : undefined,
          scorersSummary: resultForm.notes.trim() || undefined,
          recordedBy: currentOperator.name,
        }};
      }}
      return m;
    }}));

    // Dynamic Knockout Progression
    if (recordingResultMatch.stage === 'r32' && resultForm.status === 'finished' && sA !== sB) {{
      const pair = R32_SEED_PAIRS[recordingResultMatch.id];
      if (pair) {{
        const winnerName = sA > sB ? recordingResultMatch.teamA : recordingResultMatch.teamB;
        setMatches(prevMatches => prevMatches.map(m => {{
          if (m.id === pair.nextMatchId) {{
            return {{
              ...m,
              [pair.nextSlot]: winnerName,
            }};
          }}
          return m;
        }}));
      }}
    }}

    setRecordingResultMatch(null);
    confetti({{ particleCount: 60, spread: 70 }});
    alert('تم اعتماد نتيجة المباراة وتحديث الترتيب والنقاط تلقائياً! ⚽');
  }};

  // Save Team Edit (Single team name & group)
  const handleSaveTeamEdit = (e: React.FormEvent) => {{
    e.preventDefault();
    if (!editingTeam) return;

    const oldName = teams.find(t => t.id === editingTeam.id)?.name || editingTeam.name;
    const newName = editingTeam.name.trim();
    if (!newName) return;

    setTeams(prev => prev.map(t => t.id === editingTeam.id ? editingTeam : t));

    if (oldName !== newName) {{
      setMatches(prev => prev.map(m => ({{
        ...m,
        teamA: m.teamA === oldName ? newName : m.teamA,
        teamB: m.teamB === oldName ? newName : m.teamB,
      }})));
    }}

    setEditingTeam(null);
    confetti({{ particleCount: 50, spread: 60 }});
    alert('تم حفظ وتحديث بيانات الفريق بنجاح! ✨');
  }};

  // Standings helper: dynamically computes stats from finished matches
  const getGroupStandings = (groupLetter: string) => {{
    return teams
      .filter(t => t.group === groupLetter)
      .map(team => {{
        const finishedTeamMatches = matches.filter(
          m => m.stage === 'group' && m.group === groupLetter && m.status === 'finished' &&
          (m.teamA === team.name || m.teamB === team.name) &&
          m.scoreA !== null && m.scoreB !== null
        );

        const played = finishedTeamMatches.length;
        let won = 0;
        let drawn = 0;
        let lost = 0;
        let gf = 0;
        let ga = 0;

        finishedTeamMatches.forEach(m => {{
          const isA = m.teamA === team.name;
          const myScore = isA ? m.scoreA! : m.scoreB!;
          const oppScore = isA ? m.scoreB! : m.scoreA!;
          gf += myScore;
          ga += oppScore;
          if (myScore > oppScore) won++;
          else if (myScore === oppScore) drawn++;
          else lost++;
        }});

        const gd = gf - ga;
        const points = won * 3 + drawn;

        return {{
          ...team,
          played,
          won,
          drawn,
          lost,
          gf,
          ga,
          gd,
          points,
        }};
      }})
      .sort((a, b) => {{
        if (b.points !== a.points) return b.points - a.points;
        if (b.gd !== a.gd) return b.gd - a.gd;
        if (b.gf !== a.gf) return b.gf - a.gf;
        return a.name.localeCompare(b.name, 'ar');
      }});
  }};

  // Helper to project team names in Round of 32
  const resolveR32MatchTeams = (match: Match) => {{
    const pair = R32_SEED_PAIRS[match.id];
    if (!pair) return null;

    const standA = getGroupStandings(pair.groupA);
    const standB = getGroupStandings(pair.groupB);

    const teamAObj = standA[pair.rankA - 1];
    const teamBObj = standB[pair.rankB - 1];

    return {{
      teamAName: teamAObj?.name || pair.labelA,
      teamBName: teamBObj?.name || pair.labelB,
      seedA: pair.labelA,
      seedB: pair.labelB,
      isProjected: true,
    }};
  }};

  // Helper to project matchup description
  const getProjectedR32Matchup = (groupLetter: string, rank: number) => {{
    for (const [matchKey, pair] of Object.entries(R32_SEED_PAIRS)) {{
      if (pair.groupA === groupLetter && pair.rankA === rank) {{
        return `مواجهة دور 32: ضد ${{pair.labelB}} (${{matchKey}})`;
      }}
      if (pair.groupB === groupLetter && pair.rankB === rank) {{
        return `مواجهة دور 32: ضد ${{pair.labelA}} (${{matchKey}})`;
      }}
    }}
    return 'غير مؤهل لدور الـ 32';
  }};

  // Add Match Handler
  const handleAddCustomMatch = (e: React.FormEvent) => {{
    e.preventDefault();
    const newId = `custom_${{Date.now()}}`;
    const newM: Match = {{
      id: newId,
      stage: newMatchForm.stage,
      stageName: newMatchForm.stageName,
      teamA: newMatchForm.teamA,
      teamB: newMatchForm.teamB,
      scoreA: null,
      scoreB: null,
      status: 'upcoming',
      date: newMatchForm.date,
      time: newMatchForm.time,
      pitch: newMatchForm.pitch,
      isScheduled: Boolean(newMatchForm.date), // Only scheduled if date entered
      recordedBy: currentOperator.name,
    }};

    setMatches(prev => [newM, ...prev]);
    setIsAddingMatch(false);
    confetti({{ particleCount: 50, spread: 60 }});
    alert('تمت إضافة المباراة بنجاح! ⚽');
  }};

  // Add Scorekeeper Handler
  const handleAddScorekeeper = (e: React.FormEvent) => {{
    e.preventDefault();
    if (!newScorekeeperForm.name || !newScorekeeperForm.studentId) return;

    const newSK: Scorekeeper = {{
      id: `sk_${{Date.now()}}`,
      name: newScorekeeperForm.name,
      studentId: newScorekeeperForm.studentId,
      role: 'scorekeeper',
      assignedGroups: ['ALL'],
      active: true,
    }};

    setScorekeepers(prev => [...prev, newSK]);
    setNewScorekeeperForm({{ name: '', studentId: '', assignedGroups: 'ALL' }});
    confetti({{ particleCount: 40, spread: 60 }});
    alert('تم تفويض مسؤول النتائج الجديد بنجاح!');
  }};

  // Bulk Edit Handlers
  const handleOpenBulkEditModal = () => {{
    const groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
    const map: Record<string, string[]> = {{}};
    let fullTextLines: string[] = [];

    groups.forEach(grp => {{
      const gTeams = teams.filter(t => t.group === grp);
      map[grp] = [];
      fullTextLines.push(`=== المجموعة ${{grp}} ===`);
      for (let i = 0; i < 6; i++) {{
        const tName = gTeams[i]?.name || `فريق ${{i + 1}} (${{grp}})`;
        map[grp].push(tName);
        fullTextLines.push(`${{i + 1}}. ${{tName}}`);
      }}
      fullTextLines.push('');
    }});

    setBulkTeamsByGroup(map);
    setBulkTeamsText(fullTextLines.join('\\n'));
    setBulkEditTab('by_group');
    setIsBulkEditingTeams(true);
  }};

  const handleApplyPastedTeamsText = () => {{
    const rawLines = bulkTeamsText.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
    const cleanedNames: string[] = [];

    rawLines.forEach(line => {{
      if (line.includes('===') || line.includes('المجموعة') || line.includes('Group')) return;
      let clean = line.replace(/^[0-9]+[\.\-\)\s]+/, '').trim();
      if (clean) cleanedNames.push(clean);
    }});

    const groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
    const newMap: Record<string, string[]> = {{}};
    let cursor = 0;

    groups.forEach(grp => {{
      newMap[grp] = [];
      for (let i = 0; i < 6; i++) {{
        if (cursor < cleanedNames.length) {{
          newMap[grp].push(cleanedNames[cursor]);
          cursor++;
        }} else {{
          newMap[grp].push(`فريق ${{i + 1}} (${{grp}})`);
        }}
      }}
    }});

    setBulkTeamsByGroup(newMap);
    setBulkEditTab('by_group');
  }};

  const handleSaveBulkTeams = (updatedByGroup: Record<string, string[]>) => {{
    const groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
    const newTeams: Team[] = [];
    const renameMap: Record<string, string> = {{}};

    groups.forEach(grp => {{
      const currentGTeams = teams.filter(t => t.group === grp);
      const newNames = updatedByGroup[grp] || [];

      for (let i = 0; i < 6; i++) {{
        const existing = currentGTeams[i];
        const newName = (newNames[i] || '').trim() || (existing ? existing.name : `فريق ${{i + 1}} (${{grp}})`);
        const id = existing ? existing.id : `t_${{grp.toLowerCase()}}_${{i + 1}}`;
        const logoColor = existing ? existing.logoColor : 'from-emerald-600 to-teal-500';

        if (existing && existing.name !== newName) {{
          renameMap[existing.name] = newName;
        }}

        newTeams.push({{
          id,
          name: newName,
          group: grp,
          played: existing ? existing.played : 0,
          won: existing ? existing.won : 0,
          drawn: existing ? existing.drawn : 0,
          lost: existing ? existing.lost : 0,
          gf: existing ? existing.gf : 0,
          ga: existing ? existing.ga : 0,
          gd: existing ? existing.gd : 0,
          points: existing ? existing.points : 0,
          logoColor,
        }});
      }}
    }});

    setTeams(newTeams);

    if (Object.keys(renameMap).length > 0) {{
      setMatches(prev => prev.map(m => ({{
        ...m,
        teamA: renameMap[m.teamA] || m.teamA,
        teamB: renameMap[m.teamB] || m.teamB,
      }})));
    }}

    setIsBulkEditingTeams(false);
    confetti({{ particleCount: 60, spread: 70 }});
    alert('تم حفظ وتحديث أسماء الفرق والجدول بالكامل! 🏆');
  }};

  // Filtered Matches based on Schedule status & filters
  const filteredMatches = useMemo(() => {{
    return matches.filter(m => {{
      // 1. Schedule Status filter (scheduled vs unscheduled vs all)
      if (matchScheduleTab === 'scheduled' && !m.isScheduled) return false;
      if (matchScheduleTab === 'unscheduled' && m.isScheduled) return false;

      // 2. Status filter
      if (matchFilterStatus !== 'all' && m.status !== matchFilterStatus) return false;

      // 3. Stage filter
      if (matchStageFilter === 'group' && m.stage !== 'group') return false;
      if (matchStageFilter === 'r32' && m.stage !== 'r32') return false;
      if (matchStageFilter === 'r16' && m.stage !== 'r16') return false;
      if (matchStageFilter === 'finals' && !['qf', 'sf', 'final'].includes(m.stage)) return false;

      // 4. Group stage round filter
      if (groupStageRoundFilter !== 'all' && m.round !== groupStageRoundFilter) return false;

      // 5. Group stage letter filter
      if (groupStageLetterFilter !== 'all' && m.group !== groupStageLetterFilter) return false;

      // 6. Search query
      if (searchQuery.trim()) {{
        const q = searchQuery.toLowerCase();
        const a = m.teamA.toLowerCase();
        const b = m.teamB.toLowerCase();
        const s = m.stageName.toLowerCase();
        if (!a.includes(q) && !b.includes(q) && !s.includes(q)) return false;
      }}

      return true;
    }});
  }}, [matches, matchScheduleTab, matchFilterStatus, matchStageFilter, groupStageRoundFilter, groupStageLetterFilter, searchQuery]);

  const scheduledMatchesCount = useMemo(() => matches.filter(m => m.isScheduled).length, [matches]);
  const unscheduledMatchesCount = useMemo(() => matches.filter(m => !m.isScheduled).length, [matches]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-emerald-500 selection:text-white" dir="rtl">
      
      {/* Top Header / App Navigation */}
      <header className="sticky top-0 z-40 bg-slate-950/90 backdrop-blur-md border-b border-emerald-950/80 px-4 md:px-8 py-3.5 shadow-2xl">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
          
          {/* Logo & Main Title */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 ring-2 ring-emerald-400/20">
              <Trophy className="w-5 h-5 text-slate-950" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-black text-lg md:text-xl text-white tracking-wide">
                  دوري جامعة النيل 2026
                </h1>
                <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[10px] font-bold">
                  48 فريقاً • 8 مجموعات
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-medium">
                نظام إلكتروني لإدارة وتحديد مواعيد ونتائج المباريات وتأهل دور الـ 32
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex flex-wrap items-center gap-1.5 bg-slate-950 p-1.5 rounded-2xl border border-slate-800">
            <button
              onClick={() => setCurrentTab('matches_control')}
              className={`px-3.5 py-2 rounded-xl text-xs md:text-sm font-bold flex items-center gap-1.5 transition-all cursor-pointer ${{
                currentTab === 'matches_control'
                  ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-lg shadow-emerald-600/30'
                  : 'bg-slate-900/80 text-slate-300 hover:bg-slate-800'
              }}`}
            >
              <Calendar className="w-4 h-4" />
              المباريات وجدول المواعيد ({scheduledMatchesCount})
            </button>

            <button
              onClick={() => setCurrentTab('groups')}
              className={`px-3.5 py-2 rounded-xl text-xs md:text-sm font-bold flex items-center gap-1.5 transition-all cursor-pointer ${{
                currentTab === 'groups'
                  ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/30'
                  : 'bg-slate-900/80 text-slate-300 hover:bg-slate-800'
              }}`}
            >
              <Shield className="w-4 h-4" />
              المجموعات (تأهل 32 فريق)
            </button>

            <button
              onClick={() => setCurrentTab('bracket')}
              className={`px-3.5 py-2 rounded-xl text-xs md:text-sm font-bold flex items-center gap-1.5 transition-all cursor-pointer ${{
                currentTab === 'bracket'
                  ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/30'
                  : 'bg-slate-900/80 text-slate-300 hover:bg-slate-800'
              }}`}
            >
              <Swords className="w-4 h-4" />
              شجرة البطولة (دور 32 حتى النهائي)
            </button>

            <button
              onClick={() => setCurrentTab('manage')}
              className={`px-3.5 py-2 rounded-xl text-xs md:text-sm font-bold flex items-center gap-1.5 transition-all cursor-pointer ${{
                currentTab === 'manage'
                  ? 'bg-amber-500 text-slate-950 font-black shadow-lg shadow-amber-500/30'
                  : 'bg-slate-900/80 text-amber-400 border border-amber-500/30 hover:bg-slate-800'
              }}`}
            >
              <SlidersHorizontal className="w-4 h-4" />
              إدارة الفرق والمجاميع
            </button>
          </nav>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 flex flex-col gap-6">

        {/* ========================================================================= */}
        {/* TAB 1: MATCHES & SCHEDULING CONTROL */}
        {/* ========================================================================= */}
        {{currentTab === 'matches_control' && (
          <div className="space-y-6">
            
            {/* Header Banner */}
            <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-emerald-950 via-[#062411] to-slate-900 border border-emerald-500/30 p-6 md:p-8 shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold mb-2">
                  <Clock className="w-3.5 h-3.5 text-emerald-400" />
                  التحكم في مواعيد وتنزيل المباريات وتسجيل النتائج
                </div>
                <h2 className="text-xl md:text-3xl font-black text-white mb-2">
                  جدول المباريات: لا ينزل أي ماتش إلا بعد تحديد موعده وملعبه
                </h2>
                <p className="text-xs md:text-sm text-slate-300 max-w-2xl leading-relaxed">
                  يمكنك مراجعة المباريات غير المجدولة، وتحديد تاريخ وساعة وملعب كل مباراة لتنزل رسمياً في الجدول، وتسجيل النتائج المباشرة والنهائية وتحديث الترتيب فوراً.
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-3 shrink-0">
                <button
                  onClick={handleResetAllMatches}
                  className="px-4 py-3 rounded-2xl bg-rose-500/10 hover:bg-rose-600 text-rose-300 hover:text-white border border-rose-500/30 hover:border-rose-600 font-bold text-xs md:text-sm flex items-center gap-2 transition-all cursor-pointer shadow-lg"
                  title="تصفير كل الماتشات والنتائج وإعادة النقاط لصفر"
                >
                  <RotateCcw className="w-4 h-4 text-rose-400" />
                  صفر كل الماتشات
                </button>
                <button
                  onClick={() => setIsAddingMatch(true)}
                  className="px-5 py-3 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-black text-xs md:text-sm shadow-xl shadow-emerald-500/20 flex items-center gap-2 transition-all cursor-pointer"
                >
                  <Plus className="w-4 h-4" />
                  إضافة مباراة مخصصة
                </button>
              </div>
            </div>

            {/* Main Scheduling Filter Segment (المباريات المنشورة vs بانتظار تحديد الموعد) */}
            <div className="bg-slate-900 border border-slate-800 p-2 rounded-2xl shadow-xl flex flex-wrap items-center justify-between gap-3">
              <div className="flex flex-wrap items-center gap-2">
                <button
                  onClick={() => setMatchScheduleTab('scheduled')}
                  className={`px-4 py-2.5 rounded-xl text-xs md:text-sm font-bold flex items-center gap-2 transition-all cursor-pointer ${{
                    matchScheduleTab === 'scheduled'
                      ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/30 font-black'
                      : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                  }}`}
                >
                  <CheckCircle2 className="w-4 h-4 text-emerald-300" />
                  <span>المباريات المنشورة والمحددة الموعد</span>
                  <span className="px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 text-xs border border-emerald-500/30">
                    {{scheduledMatchesCount}}
                  </span>
                </button>

                <button
                  onClick={() => setMatchScheduleTab('unscheduled')}
                  className={`px-4 py-2.5 rounded-xl text-xs md:text-sm font-bold flex items-center gap-2 transition-all cursor-pointer ${{
                    matchScheduleTab === 'unscheduled'
                      ? 'bg-amber-500 text-slate-950 shadow-lg shadow-amber-500/30 font-black'
                      : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                  }}`}
                >
                  <Clock className="w-4 h-4 text-amber-500" />
                  <span>مباريات بانتظار تحديد الموعد</span>
                  <span className="px-2 py-0.5 rounded-full bg-amber-950 text-amber-300 text-xs border border-amber-500/30">
                    {{unscheduledMatchesCount}}
                  </span>
                </button>

                <button
                  onClick={() => setMatchScheduleTab('all')}
                  className={`px-4 py-2.5 rounded-xl text-xs md:text-sm font-bold flex items-center gap-2 transition-all cursor-pointer ${{
                    matchScheduleTab === 'all'
                      ? 'bg-slate-700 text-white shadow font-bold'
                      : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                  }}`}
                >
                  <Layers className="w-4 h-4" />
                  <span>جميع المباريات ({{matches.length}})</span>
                </button>
              </div>

              {/* Status overview chip */}
              <div className="text-xs text-slate-400 font-mono px-3 py-1.5 bg-slate-950 rounded-xl border border-slate-800">
                المعروض حالياً: <strong className="text-white">{{filteredMatches.length}}</strong> مباراة
              </div>
            </div>

            {/* Secondary Filter & Search Bar */}
            <div className="space-y-3 bg-slate-900/80 p-4 rounded-2xl border border-slate-800 shadow-md">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex flex-wrap items-center gap-1.5 text-xs">
                  <span className="text-slate-400 font-bold ml-1 flex items-center gap-1">
                    <Filter className="w-3.5 h-3.5 text-emerald-400" />
                    المرحلة:
                  </span>
                  {[
                    {{ id: 'all', label: 'جميع المراحل' }},
                    {{ id: 'group', label: 'دور المجموعات' }},
                    {{ id: 'r32', label: 'دور الـ 32' }},
                    {{ id: 'r16', label: 'دور الـ 16' }},
                    {{ id: 'finals', label: 'الأدوار النهائية 🏆' }},
                  ].map((st) => (
                    <button
                      key={{st.id}}
                      onClick={() => setMatchStageFilter(st.id as any)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${{
                        matchStageFilter === st.id
                          ? 'bg-emerald-600 text-white shadow'
                          : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                      }}`}
                    >
                      {{st.label}}
                    </button>
                  ))}
                </div>

                {/* Search */}
                <div className="relative w-full sm:w-64">
                  <input
                    type="text"
                    placeholder="ابحث عن اسم أي فرقة..."
                    value={{searchQuery}}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 pr-9 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                  />
                  <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
                </div>
              </div>

              {/* Sub-Filters for Group Stage */}
              {{matchStageFilter === 'group' && (
                <div className="pt-2 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs">
                  <div className="flex flex-wrap items-center gap-1.5">
                    <span className="text-slate-400 font-bold ml-1">المجموعة:</span>
                    <button
                      onClick={() => setGroupStageLetterFilter('all')}
                      className={`px-2.5 py-1 rounded-lg text-xs font-bold ${{
                        groupStageLetterFilter === 'all' ? 'bg-teal-600 text-white' : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                      }}`}
                    >
                      كل المجموعات
                    </button>
                    {['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].map(g => (
                      <button
                        key={{g}}
                        onClick={() => setGroupStageLetterFilter(g)}
                        className={`w-7 h-7 rounded-lg text-xs font-bold flex items-center justify-center ${{
                          groupStageLetterFilter === g ? 'bg-amber-500 text-slate-950 font-black' : 'bg-slate-950 text-slate-300 hover:text-white border border-slate-800'
                        }}`}
                      >
                        {{g}}
                      </button>
                    ))}
                  </div>

                  <div className="flex flex-wrap items-center gap-1.5">
                    <span className="text-slate-400 font-bold ml-1">الجولة:</span>
                    <button
                      onClick={() => setGroupStageRoundFilter('all')}
                      className={`px-2.5 py-1 rounded-lg text-xs font-bold ${{
                        groupStageRoundFilter === 'all' ? 'bg-teal-600 text-white' : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                      }}`}
                    >
                      كل الجولات
                    </button>
                    {[1, 2, 3, 4, 5].map(r => (
                      <button
                        key={{r}}
                        onClick={() => setGroupStageRoundFilter(r)}
                        className={`w-7 h-7 rounded-lg text-xs font-bold flex items-center justify-center ${{
                          groupStageRoundFilter === r ? 'bg-emerald-600 text-white' : 'bg-slate-950 text-slate-300 hover:text-white border border-slate-800'
                        }}`}
                      >
                        {{r}}
                      </button>
                    ))}
                  </div>
                </div>
              )}}
            </div>

            {/* Empty State when in 'scheduled' tab and no matches are scheduled yet */}
            {{matchScheduleTab === 'scheduled' && scheduledMatchesCount === 0 && (
              <div className="text-center py-14 px-6 bg-slate-900/80 border border-slate-800 rounded-3xl space-y-4 shadow-xl">
                <div className="w-16 h-16 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center mx-auto shadow-inner">
                  <Calendar className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-black text-white">لم يتم تنزيل أي مباريات في الجدول الرسمي بعد</h3>
                <p className="text-xs md:text-sm text-slate-400 max-w-lg mx-auto leading-relaxed">
                  وفقاً لتوجيهاتكم، لا ينزل أي ماتش في جدول المباريات حتى تقوم بتحديد موعده وملعبه يدوياً.
                  اضغط على تبويب <strong className="text-amber-400">«مباريات بانتظار تحديد الموعد»</strong> لاختيار أي مباراة وتحديد تاريخها وساعتها لتنزل فوراً!
                </p>
                <div className="pt-2">
                  <button
                    onClick={() => setMatchScheduleTab('unscheduled')}
                    className="px-6 py-3.5 rounded-2xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-black text-xs md:text-sm shadow-xl shadow-emerald-600/30 hover:scale-105 transition-all cursor-pointer inline-flex items-center gap-2"
                  >
                    <Plus className="w-4 h-4" />
                    الانتقال للمباريات وتحديد مواعيدها الآن ({{unscheduledMatchesCount}} ماتش)
                  </button>
                </div>
              </div>
            )}}

            {/* Matches Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredMatches.map((match) => {
                const r32Info = match.stage === 'r32' ? resolveR32MatchTeams(match) : null;
                const displayTeamA = r32Info ? r32Info.teamAName : match.teamA;
                const displayTeamB = r32Info ? r32Info.teamBName : match.teamB;

                return (
                  <div
                    key={{match.id}}
                    className={`rounded-2xl border transition-all p-4 flex flex-col justify-between gap-3 shadow-lg ${{
                      match.status === 'live'
                        ? 'bg-rose-950/20 border-rose-500/50 ring-1 ring-rose-500/30'
                        : match.status === 'finished'
                        ? 'bg-slate-900/90 border-slate-800'
                        : match.isScheduled
                        ? 'bg-slate-900/90 border-emerald-500/30'
                        : 'bg-slate-950 border-slate-800/80 opacity-90'
                    }}`}
                  >
                    {/* Card Header */}
                    <div className="flex items-center justify-between text-xs border-b border-slate-800/80 pb-2.5">
                      <div className="flex items-center gap-1.5">
                        <span className="px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-300 text-[11px] font-bold border border-emerald-500/20">
                          {match.stage === 'group' ? `الجولة ${match.round || 1}` : match.stageName}
                        </span>
                        {match.group && (
                          <span className="px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 text-[11px] font-bold">
                            المجموعة {match.group}
                          </span>
                        )}
                      </div>

                      {/* Schedule Badge / Status Badge */}
                      {match.isScheduled ? (
                        <div className="flex items-center gap-1 text-[11px]">
                          {match.status === 'finished' ? (
                            <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-bold">
                              انتهت FT
                            </span>
                          ) : match.status === 'live' ? (
                            <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 font-bold border border-rose-500/30 animate-pulse">
                              مباشر د{match.minute || 90}
                            </span>
                          ) : (
                            <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/30">
                              محددة في الجدول
                            </span>
                          )}
                        </div>
                      ) : (
                        <span className="px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-300 text-[11px] font-bold border border-amber-500/30 flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          لم يُحدد الموعد بعد
                        </span>
                      )}
                    </div>

                    {/* Date, Time & Pitch (or Unscheduled Hint) */}
                    <div className="text-[11px] flex items-center justify-between text-slate-400 font-mono">
                      {match.isScheduled ? (
                        <>
                          <span className="flex items-center gap-1">
                            <Calendar className="w-3 h-3 text-emerald-400" />
                            {match.date} • {match.time}
                          </span>
                          <span className="flex items-center gap-1 truncate max-w-[130px]">
                            <MapPin className="w-3 h-3 text-slate-500" />
                            {match.pitch}
                          </span>
                        </>
                      ) : (
                        <span className="text-amber-400/80 text-[11px] flex items-center gap-1 font-sans">
                          <AlertCircle className="w-3 h-3 text-amber-400" />
                          بانتظار تحديد موعد وملعب المباراة
                        </span>
                      )}
                    </div>

                    {/* Teams & Score Box */}
                    <div className="py-2.5 flex items-center justify-between px-1 bg-slate-950/60 rounded-xl border border-slate-800/60">
                      {/* Team A */}
                      <div className="flex-1 text-center font-bold text-white text-xs md:text-sm">
                        <button
                          onClick={() => setSelectedTeamNameForMatches(displayTeamA)}
                          className="hover:text-emerald-300 transition-colors cursor-pointer truncate max-w-full hover:underline font-bold inline-block"
                          title={`اضغط لعرض مباريات ${displayTeamA}`}
                        >
                          {displayTeamA}
                        </button>
                        {r32Info && (
                          <span className="block mt-1 px-2 py-0.5 rounded-md bg-emerald-500/15 text-emerald-300 text-[10px] font-bold border border-emerald-500/30 mx-auto w-fit">
                            {r32Info.seedA}
                          </span>
                        )}
                      </div>

                      {/* Score or VS */}
                      <div className="px-3.5 py-1.5 bg-slate-900 border border-slate-800 rounded-xl text-center min-w-[75px] shadow-inner mx-2">
                        {match.scoreA !== null && match.scoreB !== null ? (
                          <span className="font-mono text-lg font-black text-emerald-400">
                            {match.scoreA} - {match.scoreB}
                          </span>
                        ) : (
                          <span className="text-xs text-slate-500 font-mono font-bold">VS</span>
                        )}
                      </div>

                      {/* Team B */}
                      <div className="flex-1 text-center font-bold text-white text-xs md:text-sm">
                        <button
                          onClick={() => setSelectedTeamNameForMatches(displayTeamB)}
                          className="hover:text-emerald-300 transition-colors cursor-pointer truncate max-w-full hover:underline font-bold inline-block"
                          title={`اضغط لعرض مباريات ${displayTeamB}`}
                        >
                          {displayTeamB}
                        </button>
                        {r32Info && (
                          <span className="block mt-1 px-2 py-0.5 rounded-md bg-emerald-500/15 text-emerald-300 text-[10px] font-bold border border-emerald-500/30 mx-auto w-fit">
                            {r32Info.seedB}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Scorers / Notes summary (if any) */}
                    {match.scorersSummary && (
                      <div className="p-2 bg-slate-950/80 rounded-xl border border-slate-800/60 text-[11px] text-slate-300">
                        <span className="text-amber-400 font-bold block mb-0.5">⚽ ملاحظات / مسجلو الأهداف:</span>
                        <span>{match.scorersSummary}</span>
                      </div>
                    )}

                    {/* Card Actions */}
                    <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between gap-2">
                      <div className="flex items-center gap-1">
                        <button
                          onClick={() => handleOpenScheduleModal(match)}
                          className={`px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer ${{
                            match.isScheduled
                              ? 'bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700'
                              : 'bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-400 hover:to-yellow-400 text-slate-950 font-black shadow-md shadow-amber-500/20'
                          }}`}
                          title={match.isScheduled ? 'تعديل تاريخ وملعب المباراة' : 'تحديد الموعد والملعب وتنزيل المباراة في الجدول'}
                        >
                          <Clock className="w-3.5 h-3.5" />
                          <span>{match.isScheduled ? 'تعديل الميعاد' : 'تحديد الميعاد وتنزيل الماتش'}</span>
                        </button>
                      </div>

                      <div className="flex items-center gap-1">
                        <button
                          onClick={() => handleOpenResultModal(match)}
                          className="px-3 py-1.5 rounded-xl bg-emerald-600/20 hover:bg-emerald-600 text-emerald-300 hover:text-white border border-emerald-500/30 text-xs font-bold flex items-center gap-1 transition-all cursor-pointer shadow-sm"
                          title="تسجيل أو تعديل نتيجة المباراة"
                        >
                          <Edit3 className="w-3.5 h-3.5" />
                          <span>{match.status === 'finished' ? 'تعديل النتيجة' : 'تسجيل النتيجة'}</span>
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}}

        {/* ========================================================================= */}
        {/* TAB 2: GROUPS (48 TEAMS & QUALIFICATION TO ROUND OF 32) */}
        {/* ========================================================================= */}
        {{currentTab === 'groups' && (
          <div className="space-y-6">
            {/* Qualification Rules Announcement Banner */}
            <div className="bg-gradient-to-r from-emerald-950/60 via-slate-900 to-teal-950/60 border border-emerald-500/30 p-6 rounded-3xl shadow-2xl space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-bold mb-2">
                    <Trophy className="w-3.5 h-3.5 text-amber-400" />
                    <span>النظام الرسمي للبطولة المعتمد</span>
                  </div>
                  <h2 className="text-xl md:text-2xl font-black text-white flex items-center gap-2">
                    <span>جدول المجموعات ونظام التأهل لدور الـ 32</span>
                  </h2>
                  <p className="text-xs md:text-sm text-slate-300 mt-1 max-w-2xl leading-relaxed">
                    يصعد <strong className="text-emerald-300">أول 4 فرق من كل مجموعة</strong> (من المجموعة A وحتى H) مباشرة إلى <strong className="text-amber-300">دور الـ 32 الإقصائي</strong> (إجمالي 32 فريقاً متأهلاً). ويغادر المركزان الخامس والسادس المسابقة.
                  </p>
                </div>

                {/* Switch between Single Group Table, 5-Round Fixtures, and All 32 Qualified Teams View */}
                <div className="flex items-center gap-2 bg-slate-950/80 p-1.5 rounded-2xl border border-slate-800 self-start md:self-auto">
                  <button
                    onClick={() => setGroupsViewMode('table')}
                    className={`px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer ${{
                      groupsViewMode === 'table'
                        ? 'bg-emerald-600 text-white shadow-md'
                        : 'text-slate-400 hover:text-white'
                    }}`}
                  >
                    <Layers className="w-3.5 h-3.5" />
                    جدول الترتيب
                  </button>
                  <button
                    onClick={() => setGroupsViewMode('fixtures')}
                    className={`px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer ${{
                      groupsViewMode === 'fixtures'
                        ? 'bg-teal-600 text-white shadow-md'
                        : 'text-slate-400 hover:text-white'
                    }}`}
                  >
                    <Calendar className="w-3.5 h-3.5" />
                    مباريات المجموعة (5 جولات)
                  </button>
                  <button
                    onClick={() => setGroupsViewMode('qualified_32')}
                    className={`px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer ${{
                      groupsViewMode === 'qualified_32'
                        ? 'bg-amber-500 text-slate-950 shadow-md font-black'
                        : 'text-slate-400 hover:text-white'
                    }}`}
                  >
                    <Award className="w-3.5 h-3.5" />
                    المتأهلون الـ 32 (الكل)
                  </button>
                </div>
              </div>

              {/* Tournament Metric Chips */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 border-t border-slate-800/80">
                <div className="bg-slate-950/60 p-3 rounded-2xl border border-slate-800/80">
                  <span className="text-[11px] text-slate-400 block font-medium">مباريات كل فريق</span>
                  <strong className="text-base font-black text-white">5 مباريات (15 بالمجموعة)</strong>
                </div>
                <div className="bg-slate-950/60 p-3 rounded-2xl border border-slate-800/80">
                  <span className="text-[11px] text-slate-400 block font-medium">المباريات المنشورة</span>
                  <strong className="text-base font-black text-emerald-400">{{scheduledMatchesCount}} من أصل 120</strong>
                </div>
                <div className="bg-emerald-950/30 p-3 rounded-2xl border border-emerald-500/20">
                  <span className="text-[11px] text-emerald-300 block font-medium">المتأهلون لدور الـ 32</span>
                  <strong className="text-base font-black text-amber-400">32 فريقاً (أول 4 من كل م.)</strong>
                </div>
                <div className="bg-slate-950/60 p-3 rounded-2xl border border-slate-800/80">
                  <span className="text-[11px] text-slate-400 block font-medium">أدوار البطولة الإقصائية</span>
                  <strong className="text-base font-black text-teal-300">من دور 32 حتى النهائي 🏆</strong>
                </div>
              </div>
            </div>

            {/* MODE 1: SINGLE GROUP STANDINGS TABLE */}
            {{groupsViewMode === 'table' && (
              <div className="space-y-4">
                {/* Group Selector Bar */}
                <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-900/80 border border-slate-800 p-4 rounded-2xl shadow-lg">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-slate-400">اختر المجموعة:</span>
                    <div className="flex flex-wrap gap-1.5">
                      {['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].map(grp => (
                        <button
                          key={{grp}}
                          onClick={() => setSelectedGroup(grp)}
                          className={`w-9 h-9 rounded-xl text-xs font-black transition-all cursor-pointer flex items-center justify-center ${{
                            selectedGroup === grp
                              ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-lg shadow-emerald-600/30 ring-2 ring-emerald-400'
                              : 'bg-slate-950 text-slate-300 hover:text-white border border-slate-800 hover:border-slate-700'
                          }}`}
                        >
                          {{grp}}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center gap-3 text-xs">
                    <div className="flex items-center gap-1.5">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-sm shadow-emerald-500/50"></span>
                      <span className="text-slate-300 font-bold">المراكز 1-4: صعود لدور الـ 32</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
                      <span className="text-slate-400">المراكز 5-6: إقصاء</span>
                    </div>
                  </div>
                </div>

                {/* Table */}
                <div className="bg-slate-900/90 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl">
                  <div className="p-4 bg-slate-950/60 border-b border-slate-800 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
                      <h3 className="font-black text-white text-base">ترتيب المجموعة {{selectedGroup}}</h3>
                      <span className="text-xs text-slate-400">(6 فرق تتنافس على 4 بطاقات صعود)</span>
                    </div>
                    <span className="text-xs font-bold text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
                      يصعد أول 4 إلى دور الـ 32
                    </span>
                  </div>

                  <div className="overflow-x-auto">
                    <table className="w-full text-right text-xs md:text-sm">
                      <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800 text-[11px]">
                        <tr>
                          <th className="py-3 px-4 text-center">المركز</th>
                          <th className="py-3 px-4">الفريق (اضغط لعرض مبارياته)</th>
                          <th className="py-3 px-3">حالة التأهل لدور الـ 32</th>
                          <th className="py-3 px-3 text-center">لعب</th>
                          <th className="py-3 px-3 text-center">فاز</th>
                          <th className="py-3 px-3 text-center">تعادل</th>
                          <th className="py-3 px-3 text-center">خسر</th>
                          <th className="py-3 px-3 text-center">له</th>
                          <th className="py-3 px-3 text-center">عليه</th>
                          <th className="py-3 px-3 text-center">الفارق</th>
                          <th className="py-3 px-4 text-center font-black text-emerald-400">النقاط</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60">
                        {getGroupStandings(selectedGroup).map((team, idx) => {
                          const isQualified = idx < 4;
                          const rank = idx + 1;
                          const projectedMatchup = getProjectedR32Matchup(selectedGroup, rank);

                          return (
                            <tr
                              key={team.id}
                              className={`transition-colors ${
                                isQualified
                                  ? 'bg-emerald-950/10 hover:bg-emerald-950/25 border-r-4 border-r-emerald-500'
                                  : 'hover:bg-slate-800/30 border-r-4 border-r-rose-900/40 opacity-80'
                              }`}
                            >
                              {/* Rank */}
                              <td className="py-3.5 px-4 text-center">
                                <span
                                  className={`inline-flex items-center justify-center w-7 h-7 rounded-xl font-black text-xs ${
                                    isQualified
                                      ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                                      : 'bg-slate-800 text-slate-400'
                                  }`}
                                >
                                  {rank}
                                </span>
                              </td>

                              {/* Team Name */}
                              <td className="py-3.5 px-4 font-bold text-white">
                                <button
                                  onClick={() => setSelectedTeamNameForMatches(team.name)}
                                  className="flex items-center gap-2 text-right hover:text-emerald-300 transition-colors cursor-pointer group"
                                  title="اضغط لعرض جميع مباريات هذا الفريق (5 مباريات)"
                                >
                                  <div className={`w-6 h-6 rounded-md bg-gradient-to-tr ${team.logoColor} flex items-center justify-center font-black text-[10px] text-white shrink-0 group-hover:scale-110 transition-transform`}>
                                    {team.name.charAt(0)}
                                  </div>
                                  <span className="group-hover:underline underline-offset-4">{team.name}</span>
                                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 group-hover:bg-emerald-500/20 group-hover:text-emerald-300 border border-slate-700 flex items-center gap-1 transition-colors">
                                    <Eye className="w-3 h-3" />
                                    الماتشات
                                  </span>
                                  {isQualified && (
                                    <span className="text-[10px] text-amber-400 font-normal">
                                      {rank === 1 && '🥇'}
                                      {rank === 2 && '🥈'}
                                      {rank === 3 && '🥉'}
                                      {rank === 4 && '⭐'}
                                    </span>
                                  )}
                                </button>
                              </td>

                              {/* Qualification Badge & Projected Matchup */}
                              <td className="py-3.5 px-3">
                                {isQualified ? (
                                  <div className="space-y-0.5">
                                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[11px] font-black border border-emerald-500/40">
                                      <Check className="w-3 h-3" />
                                      صعود لدور الـ 32
                                    </span>
                                    <div className="text-[10px] text-slate-400 font-medium">
                                      {projectedMatchup}
                                    </div>
                                  </div>
                                ) : (
                                  <span className="text-[11px] text-slate-500">
                                    مغادرة البطولة
                                  </span>
                                )}
                              </td>

                              {/* Standings Numbers */}
                              <td className="py-3.5 px-3 text-center font-mono font-bold text-slate-200">{team.played}</td>
                              <td className="py-3.5 px-3 text-center font-mono font-bold text-emerald-400">{team.won}</td>
                              <td className="py-3.5 px-3 text-center font-mono font-bold text-amber-400">{team.drawn}</td>
                              <td className="py-3.5 px-3 text-center font-mono font-bold text-rose-400">{team.lost}</td>
                              <td className="py-3.5 px-3 text-center font-mono text-slate-300">{team.gf}</td>
                              <td className="py-3.5 px-3 text-center font-mono text-slate-400">{team.ga}</td>
                              <td className={`py-3.5 px-3 text-center font-mono font-bold ${team.gd > 0 ? 'text-emerald-400' : team.gd < 0 ? 'text-rose-400' : 'text-slate-400'}`}>
                                {team.gd > 0 ? `+${team.gd}` : team.gd}
                              </td>
                              <td className="py-3.5 px-4 text-center font-mono font-black text-base text-amber-400 bg-slate-950/40">
                                {team.points}
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}}

            {/* MODE 2: 5-ROUNDS GROUP FIXTURES */}
            {{groupsViewMode === 'fixtures' && (
              <div className="space-y-4">
                {/* Group Selector Bar */}
                <div className="flex items-center justify-between gap-3 bg-slate-900/80 border border-slate-800 p-4 rounded-2xl">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-slate-400">اختر المجموعة:</span>
                    <div className="flex flex-wrap gap-1.5">
                      {['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].map(grp => (
                        <button
                          key={grp}
                          onClick={() => setSelectedGroup(grp)}
                          className={`w-9 h-9 rounded-xl text-xs font-black transition-all cursor-pointer flex items-center justify-center ${
                            selectedGroup === grp
                              ? 'bg-teal-600 text-white shadow-lg ring-2 ring-teal-400'
                              : 'bg-slate-950 text-slate-300 hover:text-white border border-slate-800'
                          }`}
                        >
                          {grp}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                {/* 5 Rounds List */}
                <div className="space-y-5">
                  {[1, 2, 3, 4, 5].map(roundNum => {
                    const roundMatches = matches.filter(
                      m => m.stage === 'group' && m.group === selectedGroup && m.round === roundNum
                    );

                    return (
                      <div key={roundNum} className="bg-slate-900/90 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-3">
                        <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
                          <div className="flex items-center gap-2">
                            <span className="w-7 h-7 rounded-xl bg-amber-500 text-slate-950 font-black text-xs flex items-center justify-center shadow-md">
                              {roundNum}
                            </span>
                            <h3 className="font-black text-white text-sm md:text-base">
                              الجولة {roundNum} • المجموعة {selectedGroup}
                            </h3>
                            <span className="text-xs text-slate-400">(3 مباريات يخوض فيها كل فريق مباراته رقم {roundNum})</span>
                          </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                          {roundMatches.map(m => (
                            <div key={m.id} className="bg-slate-950/80 border border-slate-800/80 hover:border-emerald-500/40 rounded-2xl p-3.5 space-y-2.5 transition-all">
                              <div className="flex items-center justify-between text-[11px] text-slate-400 border-b border-slate-800/60 pb-1.5">
                                {m.isScheduled ? (
                                  <span className="flex items-center gap-1 font-mono text-emerald-400">
                                    <Clock className="w-3 h-3" />
                                    {m.date} • {m.time}
                                  </span>
                                ) : (
                                  <span className="text-amber-400 text-[10px] font-bold">
                                    لم يُحدد الموعد بعد
                                  </span>
                                )}
                                <div>
                                  {m.status === 'finished' ? (
                                    <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-bold text-[10px]">
                                      انتهت FT
                                    </span>
                                  ) : m.status === 'live' ? (
                                    <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 font-bold text-[10px] animate-pulse">
                                      مباشر ({m.minute}')
                                    </span>
                                  ) : m.isScheduled ? (
                                    <span className="px-2 py-0.5 rounded-full bg-blue-500/15 text-blue-300 font-bold text-[10px]">
                                      مجدولة
                                    </span>
                                  ) : (
                                    <button
                                      onClick={() => handleOpenScheduleModal(m)}
                                      className="px-2 py-0.5 rounded-full bg-amber-500/20 hover:bg-amber-500 text-amber-300 hover:text-slate-950 font-bold text-[10px] border border-amber-500/30 cursor-pointer transition-colors"
                                    >
                                      تحديد الميعاد
                                    </button>
                                  )}
                                </div>
                              </div>

                              <div className="py-1 space-y-1">
                                <div className="flex items-center justify-between text-xs font-bold text-white">
                                  <button
                                    onClick={() => setSelectedTeamNameForMatches(m.teamA)}
                                    className="truncate hover:text-emerald-300 transition-colors cursor-pointer hover:underline text-right"
                                    title={`اضغط لعرض مباريات ${m.teamA}`}
                                  >
                                    {m.teamA}
                                  </button>
                                  <span className="font-mono text-emerald-400 text-sm">{m.scoreA !== null ? m.scoreA : '-'}</span>
                                </div>
                                <div className="flex items-center justify-between text-xs font-bold text-white">
                                  <button
                                    onClick={() => setSelectedTeamNameForMatches(m.teamB)}
                                    className="truncate hover:text-emerald-300 transition-colors cursor-pointer hover:underline text-right"
                                    title={`اضغط لعرض مباريات ${m.teamB}`}
                                  >
                                    {m.teamB}
                                  </button>
                                  <span className="font-mono text-emerald-400 text-sm">{m.scoreB !== null ? m.scoreB : '-'}</span>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}}

            {/* MODE 3: ALL 32 QUALIFIED TEAMS VIEW */}
            {{groupsViewMode === 'qualified_32' && (
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].map(grp => {
                    const standings = getGroupStandings(grp);
                    const qualified = standings.slice(0, 4);

                    return (
                      <div key={grp} className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl space-y-3">
                        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                          <strong className="text-sm font-black text-white">المجموعة {grp}</strong>
                          <span className="text-[10px] text-emerald-400 font-bold bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-500/20">
                            4 متأهلين
                          </span>
                        </div>

                        <div className="space-y-2">
                          {qualified.map((team, idx) => {
                            const rank = idx + 1;
                            const badgeColor =
                              rank === 1 ? 'text-amber-300 border-amber-500/40 bg-amber-500/10' :
                              rank === 2 ? 'text-slate-200 border-slate-500/40 bg-slate-500/10' :
                              rank === 3 ? 'text-amber-500 border-amber-600/40 bg-amber-600/10' :
                              'text-emerald-300 border-emerald-500/40 bg-emerald-500/10';
                            
                            return (
                              <div
                                key={team.id}
                                onClick={() => setSelectedTeamNameForMatches(team.name)}
                                className="bg-slate-950/70 hover:bg-slate-900/90 hover:border-emerald-500/40 cursor-pointer p-2.5 rounded-xl border border-slate-800/80 flex items-center justify-between text-xs transition-colors group"
                                title="اضغط لعرض مباريات هذا الفريق بالكامل"
                              >
                                <div className="flex items-center gap-2 min-w-0">
                                  <span className={`w-5 h-5 rounded-md text-[10px] font-black flex items-center justify-center border ${badgeColor}`}>
                                    {rank}
                                  </span>
                                  <span className="font-bold text-white truncate group-hover:text-emerald-300 transition-colors">{team.name}</span>
                                </div>
                                <div className="flex items-center gap-2 shrink-0">
                                  <span className="font-mono font-bold text-emerald-400 text-xs">{team.points} ن</span>
                                  <Eye className="w-3.5 h-3.5 text-slate-500 group-hover:text-emerald-300 transition-colors" />
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}}
          </div>
        )}}

        {/* ========================================================================= */}
        {/* TAB 3: KNOCKOUT BRACKET (دور الـ 32 وحتى المباراة النهائية) */}
        {/* ========================================================================= */}
        {{currentTab === 'bracket' && (
          <div className="space-y-6">
            <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 p-6 rounded-3xl shadow-xl space-y-5">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-bold mb-2">
                    <Swords className="w-3.5 h-3.5" />
                    <span>المسار الإقصائي الكامل (Knockout Bracket)</span>
                  </div>
                  <h2 className="text-xl md:text-2xl font-black text-white flex items-center gap-2">
                    شجرة البطولة: من دور الـ 32 حتى التتويج باللقب 🏆
                  </h2>
                  <p className="text-xs md:text-sm text-slate-300 mt-1 max-w-2xl leading-relaxed">
                    يتواجه المتأهلون الأربعة من كل مجموعة في <strong className="text-emerald-400">دور الـ 32 (16 مواجهة)</strong>، ويتأهل الفائزون تباعاً لدور الـ 16، وربع النهائي، ونصف النهائي حتى النهائي الحاسم.
                  </p>
                </div>

                {/* Quick Stage Filter Selector */}
                <div className="flex flex-wrap items-center gap-1.5 bg-slate-950 p-1.5 rounded-2xl border border-slate-800">
                  {[
                    {{ key: 'all', label: 'الكل' }},
                    {{ key: 'r32', label: 'دور الـ 32 (16 مباراة)' }},
                    {{ key: 'r16', label: 'دور الـ 16 (8 مباريات)' }},
                    {{ key: 'qf', label: 'ربع النهائي' }},
                    {{ key: 'sf', label: 'نصف النهائي' }},
                    {{ key: 'final', label: 'النهائي 🏆' }},
                  ].map((stageItem) => (
                    <button
                      key={{stageItem.key}}
                      onClick={() => setBracketStageFilter(stageItem.key as any)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${{
                        bracketStageFilter === stageItem.key
                          ? 'bg-amber-500 text-slate-950 font-black shadow-md'
                          : 'text-slate-400 hover:text-white'
                      }}`}
                    >
                      {{stageItem.label}}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Bracket Matches List */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {matches
                .filter(m => m.stage !== 'group')
                .filter(m => bracketStageFilter === 'all' ? true : m.stage === bracketStageFilter)
                .map((m) => {
                  const r32Info = m.stage === 'r32' ? resolveR32MatchTeams(m) : null;
                  const tA = r32Info ? r32Info.teamAName : m.teamA;
                  const tB = r32Info ? r32Info.teamBName : m.teamB;

                  return (
                    <div key={{m.id}} className="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-3 shadow-lg">
                      <div className="flex items-center justify-between text-[11px] text-slate-400 border-b border-slate-800 pb-2">
                        <span className="font-bold text-amber-400">{{m.stageName}}</span>
                        <span>{{m.isScheduled ? `${{m.date}} • ${{m.time}}` : 'لم يُحدد الموعد بعد'}}</span>
                      </div>

                      <div className="space-y-2">
                        <div className="p-2 bg-slate-950 rounded-xl flex items-center justify-between text-xs font-bold text-white">
                          <button onClick={() => setSelectedTeamNameForMatches(tA)} className="hover:text-emerald-300 truncate cursor-pointer">{tA}</button>
                          <span className="font-mono text-emerald-400">{m.scoreA !== null ? m.scoreA : '-'}</span>
                        </div>
                        <div className="p-2 bg-slate-950 rounded-xl flex items-center justify-between text-xs font-bold text-white">
                          <button onClick={() => setSelectedTeamNameForMatches(tB)} className="hover:text-emerald-300 truncate cursor-pointer">{tB}</button>
                          <span className="font-mono text-emerald-400">{m.scoreB !== null ? m.scoreB : '-'}</span>
                        </div>
                      </div>

                      <div className="pt-2 border-t border-slate-800 flex items-center justify-between gap-1 text-[11px]">
                        <button
                          onClick={() => handleOpenScheduleModal(m)}
                          className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white font-bold cursor-pointer"
                        >
                          {{m.isScheduled ? 'تعديل الميعاد' : 'تحديد الموعد'}}
                        </button>
                        <button
                          onClick={() => handleOpenResultModal(m)}
                          className="px-2.5 py-1 rounded-lg bg-emerald-600/20 hover:bg-emerald-600 text-emerald-300 hover:text-white font-bold cursor-pointer"
                        >
                          تسجيل النتيجة
                        </button>
                      </div>
                    </div>
                  );
                })}
            </div>
          </div>
        )}}

        {/* ========================================================================= */}
        {/* TAB 4: MANAGE TEAMS, GROUPS & SCOREKEEPERS */}
        {/* ========================================================================= */}
        {{currentTab === 'manage' && (
          <div className="space-y-6">
            
            {/* Manage Sub-tab switcher */}
            <div className="flex items-center gap-2 bg-slate-900 p-1.5 rounded-2xl border border-slate-800 max-w-md">
              <button
                onClick={() => setManageSubTab('teams')}
                className={`flex-1 py-2 rounded-xl text-xs md:text-sm font-bold flex items-center justify-center gap-2 transition-all cursor-pointer ${{
                  manageSubTab === 'teams'
                    ? 'bg-emerald-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-white'
                }}`}
              >
                <Shield className="w-4 h-4" />
                إدارة الفرق والمجاميع (48 فريق)
              </button>
              <button
                onClick={() => setManageSubTab('scorekeepers')}
                className={`flex-1 py-2 rounded-xl text-xs md:text-sm font-bold flex items-center justify-center gap-2 transition-all cursor-pointer ${{
                  manageSubTab === 'scorekeepers'
                    ? 'bg-amber-500 text-slate-950 font-black shadow-md'
                    : 'text-slate-400 hover:text-white'
                }}`}
              >
                <SlidersHorizontal className="w-4 h-4" />
                مسؤولو النتائج
              </button>
            </div>

            {/* Teams Sub-Tab */}
            {{manageSubTab === 'teams' && (
              <div className="space-y-4">
                {/* Header Filter & Action Bar */}
                <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-900/90 border border-slate-800 p-4 rounded-2xl shadow-xl">
                  {/* Group Filter Buttons */}
                  <div className="flex flex-wrap items-center gap-1.5 text-xs">
                    <span className="text-slate-400 font-bold ml-1 flex items-center gap-1">
                      <Layers className="w-3.5 h-3.5 text-emerald-400" />
                      المجموعة:
                    </span>
                    <button
                      onClick={() => setManageTeamsGroupFilter('all')}
                      className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${{
                        manageTeamsGroupFilter === 'all'
                          ? 'bg-emerald-600 text-white shadow-md'
                          : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                      }}`}
                    >
                      الكل (48 فريق)
                    </button>
                    {['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].map((grp) => (
                      <button
                        key={{grp}}
                        onClick={() => setManageTeamsGroupFilter(grp)}
                        className={`w-8 h-8 rounded-xl text-xs font-black transition-all cursor-pointer flex items-center justify-center ${{
                          manageTeamsGroupFilter === grp
                            ? 'bg-amber-500 text-slate-950 shadow-md font-black ring-2 ring-amber-300'
                            : 'bg-slate-950 text-slate-300 hover:text-white border border-slate-800'
                        }}`}
                      >
                        {{grp}}
                      </button>
                    ))}
                  </div>

                  {/* Actions */}
                  <div className="flex flex-wrap items-center gap-2">
                    <button
                      onClick={{handleResetAllMatches}}
                      className="px-3.5 py-2 rounded-xl bg-rose-500/10 hover:bg-rose-600 text-rose-300 hover:text-white border border-rose-500/30 text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer"
                      title="تصفير جميع المباريات والنتائج"
                    >
                      <RotateCcw className="w-3.5 h-3.5" />
                      تصفير كل الماتشات
                    </button>
                    <button
                      onClick={{handleOpenBulkEditModal}}
                      className="px-4 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-400 hover:to-yellow-400 text-slate-950 text-xs font-black flex items-center gap-2 shadow-lg shadow-amber-500/20 cursor-pointer transition-all"
                    >
                      <SlidersHorizontal className="w-3.5 h-3.5" />
                      تعديل وإدخال أسماء الفرق والمجاميع (Bulk Edit)
                    </button>
                  </div>
                </div>

                {/* Info summary */}
                <div className="p-3.5 rounded-2xl bg-emerald-950/20 border border-emerald-500/30 flex flex-wrap items-center justify-between gap-3 text-xs">
                  <div className="flex items-center gap-2 text-slate-300">
                    <Shield className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>
                      نظام المجموعات: <strong className="text-white">48 فريقاً</strong> موزعين على <strong className="text-amber-400">8 مجموعات (A حتى H)</strong> • يلعب كل فريق <strong className="text-emerald-300">5 مباريات</strong> مع فرق مجموعته • يصعد أول 4 فرق لدور الـ 32.
                    </span>
                  </div>
                  <span className="text-[11px] text-slate-400 bg-slate-950/60 px-2.5 py-1 rounded-xl border border-slate-800">
                    المعروض حالياً: {{teams.filter(t => manageTeamsGroupFilter === 'all' ? true : t.group === manageTeamsGroupFilter).length}} فرق
                  </span>
                </div>

                {/* Teams Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {teams
                    .filter((team) => (manageTeamsGroupFilter === 'all' ? true : team.group === manageTeamsGroupFilter))
                    .map((team) => (
                      <div
                        key={team.id}
                        className="bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 rounded-2xl p-4 flex flex-col justify-between gap-3 transition-all shadow-md group"
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div
                            onClick={() => setSelectedTeamNameForMatches(team.name)}
                            className="flex items-center gap-3 truncate cursor-pointer flex-1"
                            title="اضغط لعرض مباريات هذا الفريق بالكامل"
                          >
                            <div className={`w-11 h-11 rounded-xl bg-gradient-to-tr ${team.logoColor} flex items-center justify-center font-black text-sm text-white shrink-0 shadow-md group-hover:scale-105 transition-transform`}>
                              {team.name.charAt(0)}
                            </div>
                            <div className="truncate">
                              <strong className="text-xs md:text-sm font-bold text-white block truncate group-hover:text-emerald-400 transition-colors">{team.name}</strong>
                              <div className="flex items-center gap-2 mt-0.5">
                                <span className="px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-300 text-[10px] font-bold border border-emerald-500/20">
                                  المجموعة {team.group}
                                </span>
                              </div>
                            </div>
                          </div>

                          <div className="flex items-center gap-1.5 shrink-0">
                            <button
                              onClick={() => setSelectedTeamNameForMatches(team.name)}
                              className="px-2.5 py-1.5 rounded-xl bg-emerald-500/15 hover:bg-emerald-600 text-emerald-300 hover:text-white text-xs font-bold flex items-center gap-1 transition-colors cursor-pointer border border-emerald-500/20 shadow-sm"
                              title="عرض مباريات هذا الفريق (5 مباريات)"
                            >
                              <Eye className="w-3.5 h-3.5" />
                              الماتشات (5)
                            </button>
                            <button
                              onClick={() => setEditingTeam(team)}
                              className="px-2.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-bold flex items-center gap-1 transition-colors cursor-pointer border border-slate-700"
                              title="تعديل اسم الفريق ومجموعته"
                            >
                              <Edit3 className="w-3.5 h-3.5" />
                              تعديل
                            </button>
                          </div>
                        </div>

                        {/* Stats Progress Bar */}
                        <div className="pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400 font-mono">
                          <div className="flex items-center gap-1">
                            <span className="text-slate-500">المباريات:</span>
                            <strong className="text-white font-bold">{team.played} / 5</strong>
                          </div>

                          <div className="flex items-center gap-2">
                            <span>نقاط: <strong className="text-amber-400 font-bold">{team.points}</strong></span>
                            <span>فارق: <strong className="text-emerald-400 font-bold">{team.gd > 0 ? `+${team.gd}` : team.gd}</strong></span>
                          </div>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            )}}

            {/* Scorekeepers Sub-Tab */}
            {{manageSubTab === 'scorekeepers' && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div className="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl space-y-4">
                  <h3 className="text-base font-black text-white pb-3 border-b border-slate-800">
                    تعيين مسؤول جديد لتسجيل نتائج المباريات
                  </h3>
                  <form onSubmit={{handleAddScorekeeper}} className="space-y-3">
                    <div>
                      <label className="block text-xs font-bold text-slate-300 mb-1">اسم المسؤول / الحكم *</label>
                      <input
                        type="text"
                        required
                        placeholder="مثال: يوسف حسام"
                        value={{newScorekeeperForm.name}}
                        onChange={(e) => setNewScorekeeperForm({{ ...newScorekeeperForm, name: e.target.value }})}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-bold text-slate-300 mb-1">الرقم التعريفي (ID) *</label>
                      <input
                        type="text"
                        required
                        placeholder="مثال: 20230555"
                        value={{newScorekeeperForm.studentId}}
                        onChange={(e) => setNewScorekeeperForm({{ ...newScorekeeperForm, studentId: e.target.value }})}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-xs text-white focus:outline-none focus:border-amber-500 font-mono"
                      />
                    </div>
                    <button
                      type="submit"
                      className="w-full py-3 rounded-xl bg-amber-500 text-slate-950 font-black text-xs shadow-lg shadow-amber-500/20 cursor-pointer mt-2"
                    >
                      اعتماد وتفويض مسؤول النتائج
                    </button>
                  </form>
                </div>

                <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl space-y-3">
                  <h3 className="text-base font-black text-white pb-3 border-b border-slate-800">
                    المسؤولون المعتمدون ({{scorekeepers.length}})
                  </h3>
                  {scorekeepers.map((sk) => (
                    <div
                      key={sk.id}
                      className={`p-3.5 rounded-2xl border transition-all flex items-center justify-between gap-3 ${
                        sk.id === activeOperatorId ? 'bg-amber-950/20 border-amber-500/50' : 'bg-slate-950 border-slate-800'
                      }`}
                    >
                      <div>
                        <strong className="text-sm font-bold text-white block">{sk.name}</strong>
                        <span className="text-[11px] text-slate-400 font-mono">ID: {sk.studentId}</span>
                      </div>
                      {sk.id !== activeOperatorId && (
                        <button
                          onClick={() => setActiveOperatorId(sk.id)}
                          className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-emerald-600 text-slate-300 hover:text-white text-xs font-bold cursor-pointer"
                        >
                          الدخول باسمه
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}}
          </div>
        )}}

      </main>

      {/* ========================================================================= */}
      {/* MODAL: SCHEDULE / RESCHEDULE MATCH (تحديد وتنزيل ميعاد الماتش) */}
      {/* ========================================================================= */}
      {{schedulingMatch && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-lg w-full p-6 shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-lg font-black text-white flex items-center gap-2">
                  <CalendarDays className="w-5 h-5 text-emerald-400" />
                  <span>{{schedulingMatch.isScheduled ? 'تعديل ميعاد المباراة' : 'تحديد الموعد وتنزيل المباراة في الجدول'}}</span>
                </h3>
                <p className="text-xs text-slate-400 mt-1">
                  {{schedulingMatch.stageName}} • {{schedulingMatch.teamA}} ضد {{schedulingMatch.teamB}}
                </p>
              </div>
              <button
                onClick={() => setSchedulingMatch(null)}
                className="w-8 h-8 rounded-lg bg-slate-800 text-slate-400 hover:text-white flex items-center justify-center cursor-pointer"
              >
                ✕
              </button>
            </div>

            <form onSubmit={{handleSaveSchedule}} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-300 mb-1.5">تاريخ ويوم المباراة (Date) *</label>
                <input
                  type="date"
                  required
                  value={{scheduleForm.date}}
                  onChange={(e) => setScheduleForm({{ ...scheduleForm, date: e.target.value }})}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-emerald-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-300 mb-1.5">توقيت وساعة انطلاق المباراة (Time) *</label>
                <div className="grid grid-cols-4 gap-2 mb-2">
                  {['02:00 م', '04:00 م', '06:00 م', '08:00 م'].map(t => (
                    <button
                      type="button"
                      key={{t}}
                      onClick={() => setScheduleForm({{ ...scheduleForm, time: t }})}
                      className={`py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${{
                        scheduleForm.time === t ? 'bg-emerald-600 text-white shadow' : 'bg-slate-950 text-slate-400 border border-slate-800'
                      }}`}
                    >
                      {{t}}
                    </button>
                  ))}
                </div>
                <input
                  type="text"
                  required
                  placeholder="أو اكتب التوقيت يدوياً مثل: 04:30 م"
                  value={{scheduleForm.time}}
                  onChange={(e) => setScheduleForm({{ ...scheduleForm, time: e.target.value }})}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-300 mb-1.5">الملعب والموقع (Pitch) *</label>
                <select
                  value={{scheduleForm.pitch}}
                  onChange={(e) => setScheduleForm({{ ...scheduleForm, pitch: e.target.value }})}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-emerald-500"
                >
                  <option value="الملعب الرئيسي (A)">الملعب الرئيسي (A)</option>
                  <option value="ملعب النجيل الصناعي (B)">ملعب النجيل الصناعي (B)</option>
                  <option value="الملعب المتعدد (C)">الملعب المتعدد (C)</option>
                  <option value="ستاد جامعة النيل الرئيسي">ستاد جامعة النيل الرئيسي</option>
                </select>
              </div>

              <div className="flex items-center justify-between gap-3 pt-3 border-t border-slate-800">
                {{schedulingMatch.isScheduled && (
                  <button
                    type="button"
                    onClick={() => handleUnscheduleMatch(schedulingMatch.id)}
                    className="px-3 py-2 rounded-xl bg-rose-500/10 hover:bg-rose-600 text-rose-300 hover:text-white border border-rose-500/30 text-xs font-bold cursor-pointer"
                  >
                    سحب وإلغاء الميعاد
                  </button>
                )}}

                <div className="flex items-center gap-2 mr-auto">
                  <button
                    type="button"
                    onClick={() => setSchedulingMatch(null)}
                    className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold cursor-pointer"
                  >
                    إلغاء
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs shadow-lg shadow-emerald-600/30 cursor-pointer flex items-center gap-1.5"
                  >
                    <Check className="w-4 h-4" />
                    <span>تثبيت وتنزيل الماتش في الجدول 🚀</span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}}

      {/* ========================================================================= */}
      {/* MODAL: FAST RESULT RECORDING (تسجيل النتيجة المباشرة أو النهائية) */}
      {/* ========================================================================= */}
      {{recordingResultMatch && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-lg w-full p-6 shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-lg font-black text-white flex items-center gap-2">
                  <Edit3 className="w-5 h-5 text-emerald-400" />
                  <span>تسجيل واعتماد نتيجة المباراة</span>
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  {{recordingResultMatch.stageName}}
                </p>
              </div>
              <button
                onClick={() => setRecordingResultMatch(null)}
                className="w-8 h-8 rounded-lg bg-slate-800 text-slate-400 hover:text-white flex items-center justify-center cursor-pointer"
              >
                ✕
              </button>
            </div>

            <form onSubmit={{handleSaveMatchResult}} className="space-y-4">
              {/* Score Inputs Box */}
              <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 flex items-center justify-between gap-4">
                <div className="flex-1 text-center space-y-2">
                  <strong className="text-sm font-bold text-white block truncate">{{recordingResultMatch.teamA}}</strong>
                  <input
                    type="number"
                    min="0"
                    max="99"
                    required
                    value={{resultForm.scoreA}}
                    onChange={(e) => setResultForm({{ ...resultForm, scoreA: Number(e.target.value) }})}
                    className="w-20 text-center text-3xl font-black bg-slate-900 border border-slate-700 rounded-2xl py-2 text-emerald-400 focus:outline-none focus:border-emerald-500 font-mono mx-auto block"
                  />
                </div>

                <div className="text-slate-600 font-black text-xl font-mono">VS</div>

                <div className="flex-1 text-center space-y-2">
                  <strong className="text-sm font-bold text-white block truncate">{{recordingResultMatch.teamB}}</strong>
                  <input
                    type="number"
                    min="0"
                    max="99"
                    required
                    value={{resultForm.scoreB}}
                    onChange={(e) => setResultForm({{ ...resultForm, scoreB: Number(e.target.value) }})}
                    className="w-20 text-center text-3xl font-black bg-slate-900 border border-slate-700 rounded-2xl py-2 text-emerald-400 focus:outline-none focus:border-emerald-500 font-mono mx-auto block"
                  />
                </div>
              </div>

              {/* Status Selector */}
              <div>
                <label className="block text-xs font-bold text-slate-300 mb-1.5">حالة المباراة</label>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setResultForm({{ ...resultForm, status: 'finished' }})}
                    className={`py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${{
                      resultForm.status === 'finished' ? 'bg-emerald-600 text-white shadow font-black' : 'bg-slate-950 text-slate-400 border border-slate-800'
                    }}`}
                  >
                    صافرة النهاية (انتهت FT)
                  </button>
                  <button
                    type="button"
                    onClick={() => setResultForm({{ ...resultForm, status: 'live' }})}
                    className={`py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${{
                      resultForm.status === 'live' ? 'bg-rose-600 text-white shadow font-black' : 'bg-slate-950 text-slate-400 border border-slate-800'
                    }}`}
                  >
                    مباشر الآن (Live)
                  </button>
                </div>
              </div>

              {{resultForm.status === 'live' && (
                <div>
                  <label className="block text-xs font-bold text-slate-300 mb-1">الدقيقة الحالية</label>
                  <input
                    type="number"
                    min="1"
                    max="120"
                    value={{resultForm.minute}}
                    onChange={(e) => setResultForm({{ ...resultForm, minute: Number(e.target.value) }})}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-xs text-white font-mono"
                  />
                </div>
              )}}

              <div>
                <label className="block text-xs font-bold text-slate-300 mb-1.5">ملاحظات أو أسماء مسجلي الأهداف (اختياري)</label>
                <input
                  type="text"
                  placeholder="مثال: أحمد (د14)، علي (د77)"
                  value={{resultForm.notes}}
                  onChange={(e) => setResultForm({{ ...resultForm, notes: e.target.value }})}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setRecordingResultMatch(null)}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold cursor-pointer"
                >
                  إلغاء
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs shadow-lg shadow-emerald-600/30 cursor-pointer"
                >
                  اعتماد وحفظ النتيجة
                </button>
              </div>
            </form>
          </div>
        </div>
      )}}

      {/* ========================================================================= */}
      {/* MODAL: TEAM ALL MATCHES VIEW (عرض ماتشات الفرقة كاملة) */}
      {/* ========================================================================= */}
      {{selectedTeamNameForMatches && (() => {{
        const teamObj = teams.find(t => t.name === selectedTeamNameForMatches);
        const groupStandings = teamObj ? getGroupStandings(teamObj.group) : [];
        const dynamicTeamData = groupStandings.find(t => t.name === selectedTeamNameForMatches) || teamObj;
        
        const allTeamMatches = matches.filter(
          m => m.teamA === selectedTeamNameForMatches || m.teamB === selectedTeamNameForMatches
        );

        const displayedMatches = allTeamMatches.filter(m => {{
          if (teamMatchesModalFilter === 'scheduled') return m.isScheduled;
          if (teamMatchesModalFilter === 'finished') return m.status === 'finished' || m.status === 'live';
          return true;
        }});

        return (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-3 md:p-6 bg-slate-950/85 backdrop-blur-md overflow-y-auto">
            <div className="bg-slate-900 border border-slate-700/80 rounded-3xl max-w-4xl w-full shadow-2xl overflow-hidden my-auto animate-in fade-in zoom-in-95 duration-200">
              
              {/* Header */}
              <div className="bg-gradient-to-r from-slate-950 via-slate-900 to-emerald-950/50 p-5 md:p-6 border-b border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                  <div className={`w-14 h-14 rounded-2xl bg-gradient-to-tr ${{dynamicTeamData?.logoColor || 'from-emerald-600 to-teal-500'}} flex items-center justify-center font-black text-xl text-white shadow-xl ring-2 ring-white/10 shrink-0`}>
                    {{selectedTeamNameForMatches.charAt(0)}}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-black border border-emerald-500/30">
                        المجموعة {{dynamicTeamData?.group || 'A'}}
                      </span>
                      <span className="text-xs text-slate-400">
                        جدول مباريات الفريق الـ 5 كاملة في دور المجموعات
                      </span>
                    </div>
                    <h2 className="text-xl md:text-2xl font-black text-white flex items-center gap-2">
                      <span>مباريات فريق: {{selectedTeamNameForMatches}}</span>
                    </h2>
                  </div>
                </div>

                <div className="flex items-center gap-2 self-end md:self-auto">
                  {{dynamicTeamData && (
                    <button
                      onClick={() => setEditingTeam(dynamicTeamData)}
                      className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold flex items-center gap-1.5 transition-colors cursor-pointer border border-slate-700"
                    >
                      <Edit3 className="w-3.5 h-3.5" />
                      تعديل الفريق
                    </button>
                  )}}
                  <button
                    onClick={() => setSelectedTeamNameForMatches(null)}
                    className="w-9 h-9 rounded-xl bg-slate-800 hover:bg-rose-600 text-slate-300 hover:text-white flex items-center justify-center transition-colors cursor-pointer"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>

              {/* Stats Bar */}
              <div className="p-4 md:p-5 bg-slate-950/60 border-b border-slate-800/80">
                <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-2 text-center text-xs">
                  <div className="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-400 block">لعب</span>
                    <strong className="text-base font-black text-white">{{dynamicTeamData?.played || 0}} / 5</strong>
                  </div>
                  <div className="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-400 block">فاز</span>
                    <strong className="text-base font-black text-emerald-400">{{dynamicTeamData?.won || 0}}</strong>
                  </div>
                  <div className="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-400 block">تعادل</span>
                    <strong className="text-base font-black text-amber-400">{{dynamicTeamData?.drawn || 0}}</strong>
                  </div>
                  <div className="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-400 block">خسر</span>
                    <strong className="text-base font-black text-rose-400">{{dynamicTeamData?.lost || 0}}</strong>
                  </div>
                  <div className="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-400 block">له / عليه</span>
                    <strong className="text-sm font-black text-slate-200">{{dynamicTeamData?.gf || 0}} / {{dynamicTeamData?.ga || 0}}</strong>
                  </div>
                  <div className="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-400 block">فارق الأهداف</span>
                    <strong className={`text-base font-black ${{(dynamicTeamData?.gd || 0) > 0 ? 'text-emerald-400' : (dynamicTeamData?.gd || 0) < 0 ? 'text-rose-400' : 'text-slate-300'}}`}>
                      {{(dynamicTeamData?.gd || 0) > 0 ? `+${{dynamicTeamData?.gd}}` : dynamicTeamData?.gd || 0}}
                    </strong>
                  </div>
                  <div className="bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-500/30 col-span-2 sm:col-span-1">
                    <span className="text-[10px] text-emerald-300 block">النقاط</span>
                    <strong className="text-base font-black text-amber-400">{{dynamicTeamData?.points || 0}}</strong>
                  </div>
                </div>
              </div>

              {/* Sub Filter */}
              <div className="p-4 bg-slate-900 flex items-center justify-between gap-3 border-b border-slate-800 text-xs">
                <div className="flex items-center gap-1.5">
                  <span className="text-slate-400 font-bold ml-1">عرض:</span>
                  <button
                    onClick={() => setTeamMatchesModalFilter('all')}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${{
                      teamMatchesModalFilter === 'all' ? 'bg-emerald-600 text-white shadow' : 'bg-slate-950 text-slate-400 border border-slate-800'
                    }}`}
                  >
                    كل المباريات ({{allTeamMatches.length}})
                  </button>
                  <button
                    onClick={() => setTeamMatchesModalFilter('scheduled')}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${{
                      teamMatchesModalFilter === 'scheduled' ? 'bg-teal-600 text-white shadow' : 'bg-slate-950 text-slate-400 border border-slate-800'
                    }}`}
                  >
                    المحددة الموعد
                  </button>
                  <button
                    onClick={() => setTeamMatchesModalFilter('finished')}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${{
                      teamMatchesModalFilter === 'finished' ? 'bg-slate-700 text-white shadow' : 'bg-slate-950 text-slate-400 border border-slate-800'
                    }}`}
                  >
                    المنتهية
                  </button>
                </div>
              </div>

              {/* Matches List */}
              <div className="p-4 md:p-6 max-h-[60vh] overflow-y-auto space-y-3">
                {displayedMatches.map((m) => {
                  const isTeamA = m.teamA === selectedTeamNameForMatches;
                  const opponentName = isTeamA ? m.teamB : m.teamA;
                  const myScore = isTeamA ? m.scoreA : m.scoreB;
                  const oppScore = isTeamA ? m.scoreB : m.scoreA;

                  return (
                    <div
                      key={m.id}
                      className="bg-slate-950/80 border border-slate-800 hover:border-slate-700 rounded-2xl p-4 transition-all space-y-3"
                    >
                      <div className="flex flex-wrap items-center justify-between gap-2 text-xs border-b border-slate-900 pb-2">
                        <div className="flex items-center gap-2">
                          <span className="px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-300 font-bold border border-emerald-500/20 text-[11px]">
                            {m.stage === 'group' ? `الجولة ${m.round}` : m.stageName}
                          </span>
                          {m.isScheduled ? (
                            <span className="text-slate-300 font-mono text-[11px] flex items-center gap-1">
                              <Calendar className="w-3 h-3 text-emerald-400" />
                              {m.date} • {m.time} • {m.pitch}
                            </span>
                          ) : (
                            <span className="text-amber-400 text-[11px] font-bold">
                              لم يُحدد الموعد بعد
                            </span>
                          )}
                        </div>

                        <div>
                          {m.status === 'finished' ? (
                            <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-bold text-[10px]">
                              انتهت FT
                            </span>
                          ) : m.status === 'live' ? (
                            <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 font-bold text-[10px] animate-pulse">
                              مباشر د{m.minute}
                            </span>
                          ) : m.isScheduled ? (
                            <span className="px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 font-bold text-[10px]">
                              مجدولة
                            </span>
                          ) : (
                            <span className="px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-bold text-[10px]">
                              بانتظار تحديد الموعد
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Opponents & Score */}
                      <div className="flex items-center justify-between gap-3">
                        <div className="flex-1 flex items-center gap-2">
                          <div className="w-8 h-8 rounded-lg bg-emerald-600/30 text-emerald-300 font-black text-xs flex items-center justify-center shrink-0 border border-emerald-500/40">
                            {selectedTeamNameForMatches.charAt(0)}
                          </div>
                          <div>
                            <strong className="text-xs md:text-sm font-bold text-white block">{selectedTeamNameForMatches}</strong>
                            <span className="text-[10px] text-emerald-400">فريقك المختار</span>
                          </div>
                        </div>

                        <div className="shrink-0 text-center px-3 py-1 bg-slate-900 rounded-xl border border-slate-800 min-w-[70px]">
                          {m.scoreA !== null && m.scoreB !== null ? (
                            <span className="font-mono text-base font-black text-emerald-400">
                              {m.scoreA} - {m.scoreB}
                            </span>
                          ) : (
                            <span className="text-xs font-mono text-slate-500">VS</span>
                          )}
                        </div>

                        <div className="flex-1 flex items-center justify-end gap-2 text-left">
                          <div className="text-right">
                            <button
                              onClick={() => setSelectedTeamNameForMatches(opponentName)}
                              className="text-xs md:text-sm font-bold text-slate-200 hover:text-emerald-300 transition-colors cursor-pointer block truncate"
                            >
                              {opponentName}
                            </button>
                            <span className="text-[10px] text-slate-400">الخصم (اضغط لعرضه)</span>
                          </div>
                          <div className="w-8 h-8 rounded-lg bg-slate-800 text-slate-300 font-black text-xs flex items-center justify-center shrink-0">
                            {opponentName.charAt(0)}
                          </div>
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="pt-2 border-t border-slate-900 flex items-center justify-between gap-2">
                        <span className="text-[10px] text-slate-500">
                          {m.recordedBy ? `سُجلت بواسطة: ${m.recordedBy}` : 'مباراة ضمن البطولة'}
                        </span>
                        <div className="flex items-center gap-1.5">
                          <button
                            onClick={() => handleOpenScheduleModal(m)}
                            className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white text-[11px] font-bold border border-slate-800 flex items-center gap-1 cursor-pointer"
                          >
                            <Clock className="w-3 h-3 text-slate-400" />
                            <span>{m.isScheduled ? 'تعديل الميعاد' : 'تحديد الميعاد'}</span>
                          </button>
                          <button
                            onClick={() => handleOpenResultModal(m)}
                            className="px-2.5 py-1 rounded-lg bg-emerald-600/20 hover:bg-emerald-600 text-emerald-300 hover:text-white text-[11px] font-bold border border-emerald-500/30 flex items-center gap-1 cursor-pointer"
                          >
                            <Edit3 className="w-3 h-3" />
                            <span>تسجيل النتيجة</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Modal Footer */}
              <div className="p-4 bg-slate-950/80 border-t border-slate-800 flex items-center justify-between">
                <span className="text-xs text-slate-400">
                  إجمالي مباريات دور المجموعات لهذا الفريق: <strong className="text-emerald-400">5 مباريات كاملة</strong>
                </span>
                <button
                  onClick={() => setSelectedTeamNameForMatches(null)}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold cursor-pointer"
                >
                  إغلاق
                </button>
              </div>
            </div>
          </div>
        );
      }})()}}

      {/* ========================================================================= */}
      {/* MODAL: EDIT TEAM */}
      {/* ========================================================================= */}
      {{editingTeam && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-black text-white flex items-center gap-2">
                <Edit3 className="w-4 h-4 text-emerald-400" />
                تعديل اسم الفريق ومجموعته
              </h3>
              <button
                onClick={() => setEditingTeam(null)}
                className="w-8 h-8 rounded-lg bg-slate-800 text-slate-400 hover:text-white flex items-center justify-center cursor-pointer"
              >
                ✕
              </button>
            </div>

            <form onSubmit={{handleSaveTeamEdit}} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-300 mb-1">اسم الفريق *</label>
                <input
                  type="text"
                  required
                  value={{editingTeam.name}}
                  onChange={(e) => setEditingTeam({{ ...editingTeam, name: e.target.value }})}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-emerald-500 font-bold"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-300 mb-1">المجموعة (A - H) *</label>
                <select
                  value={{editingTeam.group}}
                  onChange={(e) => setEditingTeam({{ ...editingTeam, group: e.target.value }})}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
                >
                  {['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].map(g => (
                    <option key={{g}} value={{g}}>المجموعة {{g}}</option>
                  ))}
                </select>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setEditingTeam(null)}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold cursor-pointer"
                >
                  إلغاء
                </button>
                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-lg shadow-emerald-600/30 cursor-pointer"
                >
                  حفظ التعديل
                </button>
              </div>
            </form>
          </div>
        </div>
      )}}

      {/* ========================================================================= */}
      {/* MODAL: BULK EDIT / IMPORT TEAMS ACROSS THE 8 GROUPS */}
      {/* ========================================================================= */}
      {{isBulkEditingTeams && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-3 md:p-6 bg-slate-950/85 backdrop-blur-md overflow-y-auto">
          <div className="bg-slate-900 border border-slate-700 rounded-3xl max-w-5xl w-full p-5 md:p-6 shadow-2xl space-y-4 my-auto max-h-[92vh] flex flex-col">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 shrink-0">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center shadow-md">
                  <SlidersHorizontal className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base md:text-lg font-black text-white">
                    تعديل وإدخال أسماء الفرق والمجاميع (Bulk Edit & Paste)
                  </h3>
                  <p className="text-xs text-slate-400">
                    48 فريقاً موزعين على 8 مجموعات (A حتى H) • 6 فرق بكل مجموعة
                  </p>
                </div>
              </div>

              <button
                onClick={() => setIsBulkEditingTeams(false)}
                className="w-8 h-8 rounded-xl bg-slate-800 hover:bg-rose-600 text-slate-300 hover:text-white flex items-center justify-center transition-colors cursor-pointer"
              >
                ✕
              </button>
            </div>

            {/* Modal Tabs */}
            <div className="flex items-center gap-2 bg-slate-950 p-1.5 rounded-2xl border border-slate-800 shrink-0">
              <button
                onClick={() => setBulkEditTab('by_group')}
                className={`flex-1 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${{
                  bulkEditTab === 'by_group'
                    ? 'bg-amber-500 text-slate-950 font-black shadow-md'
                    : 'text-slate-400 hover:text-white'
                }}`}
              >
                تعديل المجموعات (A إلى H)
              </button>
              <button
                onClick={() => setBulkEditTab('paste_text')}
                className={`flex-1 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${{
                  bulkEditTab === 'paste_text'
                    ? 'bg-teal-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-white'
                }}`}
              >
                لصق نصي سريع (Paste Text)
              </button>
            </div>

            {/* Modal Body */}
            <div className="flex-1 overflow-y-auto pr-1">
              {{bulkEditTab === 'by_group' && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                  {['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].map((grp) => (
                    <div key={{grp}} className="bg-slate-950 p-3.5 rounded-2xl border border-slate-800 space-y-2">
                      <div className="flex items-center justify-between pb-1.5 border-b border-slate-800">
                        <strong className="text-xs font-black text-amber-400">المجموعة {{grp}}</strong>
                        <span className="text-[10px] text-slate-500">6 فرق</span>
                      </div>
                      <div className="space-y-1.5">
                        {[0, 1, 2, 3, 4, 5].map((idx) => (
                          <div key={{idx}} className="flex items-center gap-1.5">
                            <span className="w-5 text-[10px] font-mono text-slate-500 shrink-0 text-center">
                              {{idx + 1}}
                            </span>
                            <input
                              type="text"
                              value={{bulkTeamsByGroup[grp]?.[idx] || ''}}
                              onChange={(e) => {{
                                const updated = {{ ...bulkTeamsByGroup }};
                                if (!updated[grp]) updated[grp] = [];
                                updated[grp][idx] = e.target.value;
                                setBulkTeamsByGroup(updated);
                              }}}}
                              placeholder={`فريق ${{idx + 1}}`}
                              className="w-full bg-slate-900 border border-slate-800 focus:border-amber-500 rounded-lg px-2.5 py-1 text-xs text-white"
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}}

              {{bulkEditTab === 'paste_text' && (
                <div className="space-y-3">
                  <div className="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 text-xs text-slate-300 space-y-1">
                    <p className="font-bold text-amber-300">📋 تعليمات اللصق النصي السريع:</p>
                    <p className="text-slate-400 text-[11px] leading-relaxed">
                      الصق قائمة الـ 48 فريقاً سطراً بسطر أو مجمعة بأسماء المجموعات وسيتم تحليلها وتوزيعها تلقائياً بالترتيب.
                    </p>
                  </div>

                  <textarea
                    rows={{12}}
                    value={{bulkTeamsText}}
                    onChange={(e) => setBulkTeamsText(e.target.value)}
                    placeholder="برشلونة\nانجلترا\nميلان\n..."
                    className="w-full bg-slate-950 border border-slate-800 rounded-2xl p-4 text-xs text-white font-mono placeholder-slate-600 focus:outline-none focus:border-emerald-500 leading-relaxed"
                  />

                  <div className="flex items-center justify-between">
                    <span className="text-[11px] text-slate-500">
                      عدد الأسطر: {{bulkTeamsText.split('\\n').filter(x => x.trim()).length}} سطر
                    </span>

                    <button
                      type="button"
                      onClick={{handleApplyPastedTeamsText}}
                      className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-black text-xs flex items-center gap-1.5 shadow-lg shadow-teal-600/20 cursor-pointer"
                    >
                      <span>تطبيق الأسماء وتحليلها على المجموعات الـ 8</span>
                      <ChevronRight className="w-4 h-4 rotate-180" />
                    </button>
                  </div>
                </div>
              )}}
            </div>

            {/* Modal Footer */}
            <div className="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-slate-800 shrink-0">
              <span className="text-xs text-slate-400">
                ⚡ سيتم مزامنة جدول المباريات ودور الـ 32 تلقائياً مع الأسماء الجديدة.
              </span>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setIsBulkEditingTeams(false)}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold cursor-pointer"
                >
                  إلغاء
                </button>
                <button
                  type="button"
                  onClick={() => handleSaveBulkTeams(bulkTeamsByGroup)}
                  className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-black flex items-center gap-2 shadow-lg shadow-emerald-600/30 cursor-pointer"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  حفظ وتحديث أسماء الفرق والجدول بالكامل
                </button>
              </div>
            </div>
          </div>
        </div>
      )}}

      {/* Footer */}
      <footer className="border-t border-emerald-950/80 bg-slate-950/90 py-5 px-4 text-center text-xs text-slate-500">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Trophy className="w-4 h-4 text-emerald-400" />
            <span className="font-bold text-slate-300">دوري جامعة النيل لكرة القدم 2026</span>
          </div>
          <div>
            نظام بطولة كرة القدم لـ 48 فريقاً • إدارة المواعيد والنتائج والتأهل
          </div>
        </div>
      </footer>

    </div>
  );
}}
'''

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('App.tsx rebuilt cleanly!')
