"""
PythonDBAGraphs: Graphs to help with Oracle Database Tuning
Copyright (C) 2016  Robert Taft Durrett (Bobby Durrett)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact:

bobby@bobbydurrettdba.com

simplesqlstat.py

Execution statistics for one SQL statement

"""

import myplot
import util


def simplesqlstat(sql_id, start_time, end_time, instance_number):
    q_string = """
select 
END_INTERVAL_TIME,
executions_delta,
ELAPSED_TIME_DELTA/(nonzeroexecutions*1000) ELAPSED_AVG_MS
from 
(
select 
ss.snap_id,
ss.sql_id,
ss.plan_hash_value,
sn.END_INTERVAL_TIME,
ss.executions_delta,
case ss.executions_delta when 0 then 1 else ss.executions_delta end nonzeroexecutions,
ELAPSED_TIME_DELTA
from
DBA_HIST_SQLSTAT ss,DBA_HIST_SNAPSHOT sn
where ss.sql_id = '"""
    q_string += sql_id
    q_string += """'
and ss.snap_id=sn.snap_id
and ss.INSTANCE_NUMBER = """
    q_string += instance_number
    q_string += """
and ss.INSTANCE_NUMBER=sn.INSTANCE_NUMBER and
END_INTERVAL_TIME 
between 
to_date('"""
    q_string += start_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and 
to_date('"""
    q_string += end_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
)
order by snap_id,sql_id"""
    return q_string


database, dbconnection = util.script_startup('Run statistics for one SQL id')

start_time = util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)', '01-JAN-1900 12:00:00')

end_time = util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)', '01-JAN-2200 12:00:00')

instance_number = util.input_with_default('Database Instance (1 if not RAC)', '1')

# Get user input

sql_id = util.input_with_default('SQL_ID', 'acrg0q0qtx3gr')

q = simplesqlstat(sql_id, start_time, end_time, instance_number);

r = dbconnection.run_return_flipped_results(q)

# plot query

myplot.title = "Sql_id " + sql_id + " on " + database + " database, instance " + instance_number
myplot.ylabel1 = "Number of executions"
myplot.ylabel2 = "Averaged Elapsed Milliseconds"

util.exit_no_results(r)

myplot.xdatetimes = r[0]
myplot.ylists = r[1:]

myplot.line_2subplots()
