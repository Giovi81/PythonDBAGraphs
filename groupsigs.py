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

groupsigs.py

This shows the average elapsed time and total number of executions for 
a group of SQL statements defined by their force matching signature.
A signature represents a group of queries that are the same except for their
constants. The goal of this query is to pick some group of queries 
that we care about such as the main queries the users use every day and
show their performance over time. It does hide the details of the individual
queries but may have value if we choose the best set of signatures.   

"""

import myplot
import util
import signatures

database, dbconnection = util.script_startup('Stats for SQL statments by signature')

start_time = util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)', '01-JAN-1900 12:00:00')

end_time = util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)', '01-JAN-2200 12:00:00')

instance_number = util.input_with_default('Database Instance (1 if not RAC)', '1')

queryobj = signatures.groupofsignatures()

queryobj.set_start_end_instance(start_time, end_time, instance_number)

lines = util.read_config_file(util.config_dir, database + util.groupsigs_file)

for line in lines:
    if len(line) > 0:
        queryobj.add_signature(int(line))

querytext = queryobj.build_query()

results = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(results)

# plot query

myplot.title = "SQL matching group of signatures on " + database + " database, instance " + instance_number + " elapsed versus executions"
myplot.ylabel1 = "Number of executions"
myplot.ylabel2 = "Averaged Elapsed Microseconds"

myplot.xdatetimes = results[0]
myplot.ylists = results[1:]

myplot.line_2subplots()
