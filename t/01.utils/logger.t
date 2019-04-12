#!/usr/bin/env perl

# Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
# Copyright [2016-2019] EMBL-European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


use strict;
use warnings;

use Cwd;
use Test::More;
use Test::Warn;
use Test::JSON;
use Capture::Tiny ':all';
use Bio::EnsEMBL::Hive::Utils::Formatter;
use Bio::EnsEMBL::Hive::Utils ('print_aligned_fields');

BEGIN {
    use_ok( 'Bio::EnsEMBL::Hive::Utils::Formatter' );

}

my $formatter = Bio::EnsEMBL::Hive::Utils::Formatter->new();
my $stdout = send_standard_msgs();
is_valid_json $stdout;


$formatter = Bio::EnsEMBL::Hive::Utils::Formatter->init_logger();


done_testing();
