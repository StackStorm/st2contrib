# ToDo List

Features that may be useful for the Orion pack.

## Discovery

Discovery is currently function using auto import. So the other Verbs
may not be so useful.

 [ ] Orion.Discovery: CancelDiscovery
      0: profileId (Type: System.Int32; Optional: False)

 [ ] Orion.Discovery: ImportDiscoveryResults
      0: cfg 
       (Type: SolarWinds.Orion.Core.Common.Models.DiscoveryImportConfiguration;
        Optional: False)

 [ ] Orion.Discovery: GetImportDiscoveryResultsProgress
      0: importId (Type: System.Guid; Optional: False)

 [!] List Discovery profiles (with filter) + alias.

     SELECT ProfileID, Name, Description, RunTimeInSeconds, LastRun, EngineID,
            Status, JobID, SIPPort, HopCount, SearchTimeout, SNMPTimeout,
            SNMPRetries, RepeatInterval, Active, DuplicateNodes, 
            ImportUpInterface, ImportDownInterface, ImportShutdownInterface, 
            SelectionMethod, JobTimeout, ScheduleRunAtTime, 
            ScheduleRunFrequency, StatusDescription, IsHidden, IsAutoImport
            FROM Orion.DiscoveryProfiles

## NCM

 [X] Cirrus.Nodes: AddNodeToNCM
    [ ] Cirrus.Nodes: GetAllConnectionProfiles (No args).
    [ ] Cirrus.Nodes: ValidateLoginTest
    [ ] Cirrus.Nodes: ValidateLogin
 [ ] Cirrus.ConfigArchive: ExecuteScript
 [ ] Cirrus.ConfigArchive: ConfigSearch
 [ ] Cirrus.Nodes: Diff

## NPM

 [!] node_custom_prop_list
 [!] orion_health
 [!] node_custom_prop_update

## NPM Universal Device Pollers

   See https://github.com/solarwinds/OrionSDK/wiki/NPM-Universal-Device-Pollers
