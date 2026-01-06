```bash
rm -rf ./TestResults
dotnet test --collect:"XPlat Code Coverage" --results-directory ./TestResults
reportgenerator -reports:"./TestResults/*/coverage.cobertura.xml" -targetdir:"./TestResults/CoverageReport" -reporttypes:TextSummary
cat ./TestResults/CoverageReport/Summary.txt
```

Review coverage report and note baseline.