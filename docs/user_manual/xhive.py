
import json
import os.path
import subprocess
import tempfile

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive

class HiveDiagramDirective(Directive):

    # defines the parameter the directive expects
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = True
    add_index = True

    def run(self):

        # The PipeConfig sample is shown in a literal block
        content = '\n'.join(self.content)
        code_block_node = nodes.literal_block(text=content)

        # We identify the full path of the target image file and regenerate the diagram
        current_source = self.state.document.current_source
        image_relpath = self.arguments[0]
        image_path = os.path.dirname(current_source) + os.path.sep + image_relpath
        generate_diagram(content, image_path)
        img_node = nodes.image(uri=image_relpath)

        return [code_block_node, img_node]



pipeconfig_template = """
package %s;

use strict;
use warnings;

use base ('Bio::EnsEMBL::Hive::PipeConfig::HiveGeneric_conf');

sub pipeline_analyses {
    my ($self) = @_;
    my $all_analyses = [%s];
    map {$_->{-module} = 'Bio::EnsEMBL::Hive::RunnableDB::Dummy'} @$all_analyses;
    return $all_analyses;
}

1;
"""

display_config_json = json.dumps( {
    "Graph": {
        "Pad": 0,
        "DisplayStats": 0,
        "DisplayDBIDs": 0,
        "DisplayDetails": 0,
    }
} )


def generate_diagram(pipeconfig_content, target_image_filename):

    # Only rebuild the images if eHive is present
    if "EHIVE_ROOT_DIR" not in os.environ:
        return

    # A temporary file for the JSON config
    json_fh = tempfile.NamedTemporaryFile(delete = False)
    #print "json_fh:", json_fh.name
    print >> json_fh, display_config_json
    json_fh.close()

    # eHive's default configuration file
    default_config_file = os.environ["EHIVE_ROOT_DIR"] + os.path.sep + "hive_config.json"

    # A temporary file for the sample PipeConfig
    pipeconfig_fh = tempfile.NamedTemporaryFile(suffix = '.pm', dir = os.getcwd(), delete = False)
    package_name = os.path.basename(pipeconfig_fh.name)[:-3]
    #print "pipeconfig:", pipeconfig_fh.name, package_name
    print >> pipeconfig_fh, pipeconfig_template % (package_name, pipeconfig_content)
    pipeconfig_fh.close()

    # Make sure the target directory exists
    if not os.path.exists(os.path.dirname(target_image_filename)):
        os.makedirs(os.path.dirname(target_image_filename))

    #print ["generate_graph.pl", "-pipeconfig", pipeconfig_fh.name, "-output", target_image_filename]
    graph_path = os.path.join(os.environ["EHIVE_ROOT_DIR"], "scripts", "generate_graph.pl")
    subprocess.call([graph_path, "-pipeconfig", pipeconfig_fh.name, "-output", target_image_filename, "-config_file", default_config_file, "-config_file", json_fh.name])

    os.remove(json_fh.name)
    os.remove(pipeconfig_fh.name)


def hive_setup_if_needed():
    if os.environ.get("READTHEDOCS", None) == "True":
        subprocess.call([os.environ["PWD"] + os.path.sep + "rtd_upgrade.sh"])
        os.environ["EHIVE_ROOT_DIR"] = os.path.join(os.environ["PWD"], os.path.pardir, os.path.pardir)
        os.environ["PERL5LIB"] = os.path.pathsep.join(os.path.join(os.environ["PWD"], "packages", _) for _ in ["usr/share/perl5/", "usr/lib/x86_64-linux-gnu/perl5/5.22/", "usr/lib/x86_64-linux-gnu/perl5/5.22/auto/"])

